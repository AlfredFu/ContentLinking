#coding=utf-8
from com.dao import *
from com.entity.Article import *
from com.entity.Version import *

class VersionDAO(DAO):
	def __init__(self):
		super(VersionDAO,self).__init__()

	def cleanup(self):
		sql="delete from versions_backup;"
		try:
			self.cursor_stg.execute(sql)
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)

	def backup(self):
		self.switchTableContent()

	def rollback(self):
		self.switchTableContent('versions_backup','versions')

	def switchTableContent(self,fromTable='versions',toTable='versions_backup'):
		selectsql="SELECT src_origin_id,src_provider_id,src_isenglish,des_origin_id,des_provider_id,des_isenglish FROM "+fromTable+" WHERE src_isenglish='Y' and des_isenglish='Y';"	
		cleansql="delete from %s" % toTable
		try:
			self.cursor_stg.execute(cleansql)
			self.conn_stg.commit()
			self.cursor_stg.execute(selectsql)
			addsql=""
			for row in self.cursor_stg.fetchall():
				version=Version()
				version.srcOriginId=row[0]
				version.srcProviderId=row[1]
				version.srcIsEnglish=row[2]
				version.desOriginId=row[3]
				version.desProviderId=row[4]
				version.desIsEnglish=row[5]
				addsql+="replace into "+toTable+"(src_origin_id,src_provider_id,src_isenglish,des_origin_id,des_provider_id,des_isenglish) values('%s',%s,'%s','%s',%s,'%s');" % version.toTuple()
			
			self.cursor_stg.execute(addsql)
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)

class CrossRefLinkDAO(DAO):
	def __init__(self):
		DAO.__init__(self)

	def cleanup(self):
		sql="delete from cross_ref_link_en_backup;"
		try:
			self.cursor_stg.execute(sql)
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)

	def backup(self):
		self.switchTableContent()

	def rollback(self):
		self.switchTableContent('cross_ref_link_en_backup','cross_ref_link_en')

	def switchTableContent(self,fromTable='cross_ref_link_en',toTable='cross_ref_link_en_backup'):
		selectsql="SELECT src_article_id,keyword_id,des_article_id,des_item_id,des_attachment_id,src_content_type,src_origin_id,src_provider_id,src_isenglish,des_content_type,des_origin_id,des_provider_id,des_isenglish FROM %s;" % fromTable
		cleansql="delete from %s" % toTable
		try:
			self.cursor_stg.execute(cleansql)
			self.conn_stg.commit()
			addsql=""
			self.cursor_stg.execute(selectsql)
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
				addsql+="replace into cross_ref_link_en(src_article_id,keyword_id,des_article_id,des_item_id,des_attachment_id,src_content_type,src_origin_id,src_provider_id,src_isenglish,des_content_type,des_origin_id,des_provider_id,des_isenglish) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % crossRefLink.toTuple()
			self.cursor_stg.execute(addsql)
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)

class ContentDAO(DAO):
	def __init__(self):
		super(ContentDAO,self).__init__()
		self.tableName='backup_content'

	def getAll(self):
		sql="select content,target_id,content_type,backup_time from %s" % self.tableName
		try:
			self.cursor_stg.execute(sql)
			for row in self.cursor_stg.fetchall():
				article=Article()
				article.content=row[0]
				article.id=row[1]
				article.contentType=row[2]
				yield article 
		except Exception,e:
			self.log.error(e)

	def add(self,content,targetId,contentType):
		if content and targetId and contentType:
			content=self.escape_string(content)
			sql="Replace into %s(target_id,content_type,content,backup_time)values('%s','%s','%s',NOW());" %(self.tableName,targetId,contentType,content)
			try:
				self.cursor_stg.execute(sql)
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)

	def getByTarget(self,targetId,contentType):
		if targetId and contentType:
			sql="select content,target_id,content_type from %s where target_id='%s' and content_type='%s'" %(self.tableName,targetId,contentType)
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					return row[0]
			except Exception,e:
				self.log.error(e)

	def deleteAll(self):
		sql="delete from %s" % self.tableName
		try:
			self.cursor_stg.execute(sql)
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)
