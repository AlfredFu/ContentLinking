#coding=utf-8
from com.dao import *
from com.entity.Article import *

class LncQADAO(DAO):
	def __init__(self):
		super(LncQADAO,self).__init__()

	def getAll(self):
		try:
			sql="select announceid,boardid,topic,body,origin_id,provider_id,isEnglish where display=1 and isEnglish='Y';"
			self.cursor_stg.execute(sql)
			for row in self.cursor_stg.fetchall():
				article=Article()
				article.id=row[0]
				article.boardid=row[1]
				article.title=row[2]
				article.content=row[3]
				article.originId=row[4]
				article.providerId=row[5]
				article.isEnglish=row[6]
				article.contentType=Article.CONTENT_TYPE_LNCQA
				yield article
		except Exception,e:
			self.log.error(e)
			self.log.error(sql)

	def getById(self,id):
		if id:
			sql="select announceid,boardid,topic,body,origin_id,provider_id,isEnglish where announceid=%s" % id
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					article=Article()	
					article.id=row[0]
					article.boardid=row[1]
					article.title=row[2]
					article.content=row[3]
					article.originId=row[4]
					article.providerId=row[5]
					article.isEnglish=row[6]
					article.contentType=Article.CONTENT_TYPE_LNCQA
					return article
				else:
					raise Exception("No  LNC Q&A with id %s found!" %id)
			except Exception,e:
				self.log.error(e)
				self.log.error(sql)
		

	def getByOrigin(self,originId,providerId,isEnglish):
		if originId and providerId and isEnglish:
			sql="select announceid,boardid,topic,body,origin_id,provider_id,isEnglish where origin_id='%s' and provider_id=%s and isEnglish='%s';" % (originId,providerId,isEnglish)
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					article=Article()	
					article.id=row[0]
					article.boardid=row[1]
					article.title=row[2]
					article.content=row[3]
					article.originId=row[4]
					article.providerId=row[5]
					article.isEnglish=row[6]
					article.contentType=Article.CONTENT_TYPE_LNCQA
					return article
				else:
					raise Exception("No LNC Q&A with origin_id:%s,provider_id:%s,isEnglish:%s found!" %(originId,providerId,isEnglish))
			except Exception,e:
				self.log.error(e)
				self.log.error(sql)
				
	def update(self,article):
		if article and article.content:
			article.content=article.content.replace("'","\\'")
			article.content=article.content.replace('"','\\"')
			sql="update listboard set content='%s',fetch_time=CURDATE() where announceid=%s" % (article.content,article.id)
			try:
				self.cursor_stg.execute(sql)
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)
				self.log.error(sql)
		 
