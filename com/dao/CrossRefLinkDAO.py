#coding=utf-8
from com.dao import *

class CrossRefLinkDAO(DAO):
	table='cross_ref_link_en'

	def __init__(self):
		DAO.__init__(self)

	def deleteBySrcIdContentType(self,srcId,contentType):
		if srcId and contentType:
			try:
				self.cursor_stg.execute("delete from %s where src_article_id=%s and src_content_type='%s';" % (CrossRefLinkDAO.table,srcId,contentType))
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)

	def deleteByDesIdContentType(self,desId,contentType):
		if desId and contentType:
			try:
				self.cursor_stg.execute("delete from %s where des_article_id=%s and des_content_type='%s';" % (CrossRefLinkDAO.table,desId,contentType))
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)
		
	def deleteBySrcDes(self,srcId,srcContentType,desId,desContentType,provisionNum=0,attachmentId=0):
		if srcId and srcContentType and desId and desContentType:
			sql="delete from %s where src_article_id=%s and src_content_type='%s' and des_article_id=%s and des_content_type='%s'" %(CrossRefLinkDAO.table,srcId,srcContentType,desId,desContentType)
			if provisionNum:
				sql+=(" and des_item_id=%s" % provisionNum)	
			if attachmentId:
				sql+=(" and des_attachment_id=%s" % attachmentId)
			try:
				self.cursor_stg.execute(sql)
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)
				 
	def deleteByArticleIdContentType(self,articleId,contentType):
		if articleId and contentType:
			sql="delete from %s where (des_article_id=%s and des_content_type='%s') or (src_article_id=%s and src_content_type='%s');" \
				% (CrossRefLinkDAO.table,articleId,contentType,articleId,contentType)
			try:
				self.cursor_stg.execute(sql)
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)

	def insert(self,crossRefLink):
		try:
			self.cursor_stg.execute("REPLACE INTO "+CrossRefLinkDAO.table+"(src_article_id,keyword_id,des_article_id,des_item_id,des_attachment_id) VALUES(%s,%s,%s,%s,%s)" % (crossRefLink.srcId,crossRefLink.keywordId,crossRefLink.desId,crossRefLink.desItemId,crossAttachId))
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e) 
			self.log.error("Error occured in insert() of CrossRefLinkDAO.py")

	def add(self,crossRefLink):
		try:
			if crossRefLink:
				self.cursor_stg.execute("replace into "+CrossRefLinkDAO.table+"(src_article_id,keyword_id,des_article_id,des_item_id,des_attachment_id,src_content_type,src_origin_id,src_provider_id,src_isenglish,des_content_type,des_origin_id,des_provider_id,des_isenglish) values('%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % crossRefLink.toTuple())
				self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)

	def getBySrcArticleIdContentType(self,srcArticleId,srcContentType):
		"""
		获取被文章A(由参数srcArticleId,srcContentType指定)所引用的文章的id,content_type
		"""
		if srcArticleId and srcContentType:
			sql="select des_article_id,des_content_type from %s where src_article_id=%s and src_content_type='%s';" %(CrossRefLinkDAO.table,srcArticleId,srcContentType)
			try:
				self.cursor_stg.execute(sql)
				for row in self.cursor_stg.fetchall():
					yield row
			except Exception,e:
				self.log.error(e)

	def getByDesArticleIdContentType(self,desArticleId,desContentType):
		"""
		获取引用文章A(由参数desArticleId,desContentType指定)的文章的id,content type	
		"""
		if desArticleId and desContentType:
			sql="select src_article_id,src_content_type from %s where des_article_id=%s and des_content_type='%s';" %(CrossRefLinkDAO.table,desArticleId,desContentType)
			try:
				self.cursor_stg.execute(sql)
				for row in self.cursor_stg.fetchall():
					yield row
			except Exception,e:
				self.log.error(e)
			
	def getByDesSrcId(self,desId,srcId):
		pass
	
	def getRelatedArticleId(self,id,contentType):
		try:
			sql=("SELECT des_article_id AS articleId,des_content_type as content_type FROM "+CrossRefLinkDAO.table+" WHERE src_article_id=%s and src_content_type='%s' UNION SELECT src_article_id AS articleId,src_content_type as content_type FROM "+CrossRefLinkDAO.table+" WHERE des_article_id=%s and des_content_type='%s'; ") %(id,contentType,id,contentType)
			self.cursor_stg.execute(sql)
			return self.cursor_stg.fetchall()
		except Exception,e:
			self.log.error(e)
			self.log.error(sql)

	def collectRelativeStastics(self,desOriginId,desProviderId,desIsEnglish,desContentType):
		try:
	    		sql="select des_item_id,src_content_type,count(*) from "+CrossRefLinkDAO.table+" where des_origin_id='%s' and des_provider_id=%s and des_isEnglish='%s' and des_content_type='%s' and des_item_id <>0 group by src_content_type,des_item_id order by des_item_id asc;" %(desOriginId,desProviderId,desIsEnglish,desContentType)
			#print sql
	    		self.cursor_stg.execute(sql)
	    		return self.cursor_stg.fetchall()
		except Exception,e:
	    		self.log.error(e)
			self.log.error("collectRelativeStatistics() in CrossRefLinkDAO.py")
