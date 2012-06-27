#coding=utf-8
from com.entity.Article import *
from com.dao import *

class ExNewsSummaryDAO(DAO):
	def __init__(self):
		super(ExNewsSummaryDAO,self).__init__()

	def getAll(self):
		sql="select ex_new_id,origin_id,provider_id,isEnglish,content from ex_news_summary where isEnglish='Y';"
		try:
			self.cursor_stg.execute(sql)
			for row in self.cursor_stg.fetchall():
				article=self.assemble(row)
				if article:
					yield article
		except Exception,e:
			self.log.error(e)
	
	def getById(self,id):
		if id:
			sql="select ex_new_id,origin_id,provider_id,isEnglish,content from ex_news_summary where ex_new_id=%s;" % id
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					article=self.assemble(row)
					return article
				else:
					raise Exception("No article with id:%s in table ex_news_summary is found!" % id)
			except Exception,e:
				self.log.error(e)

	def getByOrigin(self,originId,providerId,isEnglish):
		if originId and providerId and isEnglish:
			sql="select ex_new_id,origin_id,provider_id,isEnglish,content from ex_news_summary where origin_id='%s' and provider_id=%s and isEnglish='%s';" % (originId,providerId,isEnglish)
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					article=self.assemble(row)
					return article
				else:
					raise Exception("No article with originId:%s providerId:%s isEnglish:%s in table ex_news_summary is found!" % (originId,providerId,isEnglish))
			except Exception,e:
				self.log.error(e)
				

	def update(self,article):
		if article and article.id:
			updateTimeSql="update ex_news set update_timei=NOW() where id=%s" % article.id
			article.content=article.content.replace("'","\\'")
			article.content=article.content.replace('"','\\"')
			updateContentSql="update ex_news_summary set content='%s' where ex_new_id=%s;" %(article.content,article.id)
			try:
				self.cursor_stg.execute(updateTimeSql)
				self.cursor_stg.execute(updateContentSql)
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)
	def assemble(self,row):
		if row:
			article=Article()
			article.id=row[0]
			article.originId=row[1]
			article.providerId=row[2]
			article.isEnglish=row[3]
			article.content=row[4]
			article.contentType=Article.CONTENT_TYPE_SUMMARY
			return article
