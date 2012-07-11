#coding=utf-8
from com.dao import *
from com.entity.Article import *

class ModuleQADAO(DAO):
	def __init__(self):
		super(ModuleQADAO,self).__init__()

	def getAll(self):
		sql="""
			select id,title,content,origin_id,provider_id,isEnglish,ex_expert_question_id from ex_expert_answers where isEnglish='Y' and is_display=1
		"""
		try:
			self.cursor_stg.execute(sql)
			for row in self.cursor_stg.fetchall():
				article=Article()
				article.id=row[0]
				article.title=row[1]
				article.content=row[2]
				article.originId=row[3]
				article.providerId=row[4]
				article.isEnglish=row[5]
				article.questionId=row[6]
				article.contentType=Article.CONTENT_TYPE_MODULEQA
				yield article
		except Exception,e:
			self.log.error(e)
			self.log.error(sql)
			self.log.error("Exception occured in getAll() of ModuleQADAO.py")

	def getById(self,id):
		if id:	
			sql="select id,title,content,origin_id,provider_id,isEnglish,ex_expert_question_id,update_time from ex_expert_answers where id=%s" % id 
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					article=Article()
					article.id=row[0]
					article.title=row[1]
					article.content=row[2]
					article.originId=row[3]
					article.providerId=row[4]
					article.isEnglish=row[5]
					article.questionId=row[6]
					article.proDate=row[7]
					article.contentType=Article.CONTENT_TYPE_MODULEQA
					return article
				else:
					raise Exception("No question answer with id:%s was found" % id)
			except Exception,e:
				self.log.error(e)
				self.log.error(sql)

	def getByOrigin(self,originId,providerId,isEnglish):
		if originId and providerId and isEnglish:
			sql="select id,title,content,origin_id,provider_id,isEnglish,ex_expert_question_id,update_time from ex_expert_answers where origin_id='%s' and provider_id=%s and isEnglish='%s';" % (originId,providerId,isEnglish) 
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					article=Article()
					article.id=row[0]
					article.title=row[1]
					article.content=row[2]
					article.originId=row[3]
					article.providerId=row[4]
					article.isEnglish=row[5]
					article.questionId=row[6]
					article.proDate=row[7]
					article.contentType=Article.CONTENT_TYPE_MODULEQA
					return article
				else:
					raise Exception("No question answer with origin id:%s,provider id:%s,isEnglish:%s was found" % (originId,providerId,isEnglish))
			except Exception,e:
				self.log.error(e)
				self.log.error(sql)

	def update(self,article,isTransfer=False):
		if article and article.questionId and article.content:
			article.content=self.escape_string(article.content)
			
			sql1="update ex_expert_questions set update_time=NOW(),fetch_time=NOW() where id=%s" % article.questionId
			sql2="update ex_expert_answers set content='%s' where id=%s" %(article.content,article.id)		
			try:
				if isTransfer: 
					self.cursor.execute(sql1)
					self.cursor.execute(sql2)
					self.conn.commit()
				else:
					self.cursor_stg.execute(sql1)
					self.cursor_stg.execute(sql2)
					self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)
			
