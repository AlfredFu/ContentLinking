#coding=utf-8
from com.dao import *
from com.entity.Article import *

class ProfNewsletterDAO(DAO):
	def __init__(self):
		super(ProfNewsletterDAO,self).__init__()


	def getAll(self):
		sql="""select 	profNewsletter_Ext.id as id,
			      	profNewsletter_Ext.title as title,
			      	profNewsletter.editedAt,
			      	profNewsletter_Ext.content,
				profNewsletter_Ext.origin_id,
				profNewsletter_Ext.provider_id,
				profNewsletter_Ext.isEnglish, 
				profNewsletter_Ext.fk_profNewsletter_id 
			from (profNewsletter_Ext INNER JOIN profNewsletter ON profNewsletter_Ext.fk_profNewsletter_id = profNewsletter.id) 
			where isDisplay=1 and isEnglish='Y';
			"""
		try:
			self.cursor_stg.execute(sql)
			for row in self.cursor_stg.fetchall():
				article=Article()
				article.id=row[0]
				article.title=row[1]
				article.editedAt=row[2]
				article.content=row[3]
				article.originId=row[4]
				article.providerId=row[5]
				article.isEnglish=row[6]
				article.fkProfNewsletterId=row[7]
				article.contentType=Article.CONTENT_TYPE_NEWSLETTER
				yield article
		except Exception,e:
			self.log.error(e)
			self.log.error(sql)

	def getById(self,id):
		if id:
			sql="""select 	profNewsletter_Ext.id as id,
					profNewsletter_Ext.title as title,
					profNewsletter.editedAt,
					profNewsletter_Ext.content,
					profNewsletter_Ext.origin_id,
					profNewsletter_Ext.provider_id,
					profNewsletter_Ext.isEnglish,
					profNewsletter_Ext.fk_profNewsletter_id 
				from (profNewsletter_Ext INNER JOIN profNewsletter ON profNewsletter_Ext.fk_profNewsletter_id = profNewsletter.id) 
				where profNewsletter_Ext.id =%s;
				""" % id
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					article=Article()
					article.id=row[0]
					article.title=row[1]
					article.editedAt=row[2]
					article.content=row[3]
					article.originId=row[4]
					article.providerId=row[5]
					article.isEnglish=row[6]
					article.fkProfNewsletterId=row[7]
					article.contentType=Article.CONTENT_TYPE_NEWSLETTER
					return article
				else:
					raise Exception("No  professional newsletter with id %s found!" %id)
			except Exception,e:
				self.log.error(e)
				self.log.error(sql)

	def getByOrigin(self,originId,providerId,isEnglish):
		if originId and providerId and isEnglish:
			sql="""select 	profNewsletter_Ext.id as id,
					profNewsletter_Ext.title as title,
					profNewsletter.editedAt,
					profNewsletter_Ext.content,
					profNewsletter_Ext.origin_id,
					profNewsletter_Ext.provider_id,
					profNewsletter_Ext.isEnglish, 
					profNewsletter_Ext.fk_profNewsletter_id 
				from (profNewsletter_Ext INNER JOIN profNewsletter ON profNewsletter_Ext.fk_profNewsletter_id = profNewsletter.id) 
				where profNewsletter_Ext.origin_id ='%s' and profNewsletter_Ext.provider_id=%s and profNewsletter_Ext.isEnglish='%s';
				""" % (originId,providerId,isEnglish)
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					article=Article()
					article.id=row[0]
					article.title=row[1]
					article.editedAt=row[2]
					article.content=row[3]
					article.originId=row[4]
					article.providerId=row[5]
					article.isEnglish=row[6]
					article.fkProfNewsletterId=row[7]
					article.contentType=Article.CONTENT_TYPE_NEWSLETTER
					return article
				else:
					raise Exception("No professional newsletter with origin_id:%s,provider_id:%s,isEnglish:%s found!" %(originId,providerId,isEnglish))
			except Exception,e:
				self.log.error(e)
				self.log.error(sql)

	def update(self,article):
		if article and article.id and article.content and article.fkProfNewsletterId:
			article.content=article.content.replace("'","\\'")
			article.content=article.content.replace('"','\\"')
			sql1="update profNewsletter set editedAt=NOW() where id=%s ;" %article.fkProfNewsletterId
			sql2="update profNewsletter set content='%s' where id=%s;" %(article.content,article.id)
			try:
				self.cursor_stg.execute(sql1)
				self.cursor_stg.execute(sql2)
				self.conn_stg.commit()	
			except Exception,e:
				self.log.error(e)
				self.log.error(sql1)
				self.log.error(sql2)
				self.log.error("Exception occured in update() of ProfNewsletterDAO.py")

if __name__=="__main__":
	dao=ProfNewsletterDAO()
	for n in dao.getAll():
		print n.fkProfNewsletterId
