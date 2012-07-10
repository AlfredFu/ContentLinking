#coding=utf-8
from com.dao import *
from com.entity.Version import *
from com.entity.CrossRefLink import *

class TransferDAO(DAO):
	def __init__(self):
		super(TransferDAO,self).__init__()
	
	def getAllVersions(self):
		sql="SELECT src_origin_id,src_provider_id,src_isenglish,des_origin_id,des_provider_id,des_isenglish FROM versions WHERE src_isenglish='Y' and des_isenglish='Y';"
		try:
			self.cursor_stg.execute(sql)
			for row in self.cursor_stg.fetchall():
				version=Version()
				version.srcOriginId=row[0]
				version.srcProviderId=row[1]
				version=srcIsEnglish=row[2]
				version.desOriginId=row[3]
				version.desProviderId=row[4]
				version.desisEnglish=row[5]
				yield version
		except Exception,e:
			self.log.error(e)

	def cleanVersions(self):
		sql="DELETE FROM versions WHERE src_isenglish='Y' AND des_isenglish='Y';"
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except Exception,e:
			self.log.error(e)

	def addVersion(self,version):
		if version:
			sql="replace into versions(src_origin_id,src_provider_id,src_isenglish,des_origin_id,des_provider_id,des_isenglish) values('%s',%s,'%s','%s',%s,'%s')" % version.toTuple()
			try:
				self.cursor.execute(sql)
				self.conn.commit()
			except Exception,e:
				self.log.error(e)

	def cleanCrossRefLinks(self):
		sql="DELETE FROM cross_ref_link_en WHERE 1;"
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except Exception,e:
			self.log.error(e)

	def getAllCrossRefLinks(self):
		sql="SELECT src_article_id,keyword_id,des_article_id,des_item_id,des_attachment_id,src_content_type,src_origin_id,src_provider_id,src_isenglish,des_content_type,des_origin_id,des_provider_id,des_isenglish FROM cross_ref_link_en"
		try:
			self.cursor_stg.execute(sql)
			for row in self.cursor_stg.fetchall():
				crossRefLink=CrossRefLink()
				crossRefLink.srcArticleId=row[0]
				crossRefLink.keywordId=row[1]
				crossRefLink.desArticleId=row[2]
				crossRefLink.desItemId=row[3]
				crossRefLink.desAttachmentId=row[4]
				crossRefLink.srcContentType=row[5]
				crossRefLink.srcOriginId=row[6]
				crossRefLink.srcProviderId=row[7]
				crossRefLink.srcIsEnglish=row[8]
				crossRefLink.desContentType=row[9]
				crossRefLink.desOriginId=row[10]
				crossRefLink.desProviderId=row[11]
				crossRefLink.desIsEnglish=row[12]
				yield crossRefLink
		except Exception,e:
			self.log.error(e)
				
		
	def addCrossRefLink(self,crossRefLink):
		if crossRefLink:
			sql="replace into cross_ref_link_en(src_article_id,keyword_id,des_article_id,des_item_id,des_attachment_id,src_content_type,src_origin_id,src_provider_id,src_isenglish,des_content_type,des_origin_id,des_provider_id,des_isenglish) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % crossRefLink.toTuple()
			try:
				self.cursor.execute(sql)
				self.conn.commit()
			except Exception,e:
				self.log.error(e)
