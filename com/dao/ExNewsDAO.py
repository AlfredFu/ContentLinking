#coding=utf-8
from com.entity.ExNews import *
from com.dao import *

class ExNewsDAO(DAO):
	"""
	操作数据库ex_news表接口
	"""

	def __init__(self):
		super(ExNewsDAO,self).__init__()

	def getAll(self):
		"""
		
		"""
		try:
			self.cursor_stg.execute("select id,origin_id,provider_id,isEnglish,title,sub_type,type,alltype,ipnews_category from ex_news where ex_news.is_display=1 and ex_news.isEnglish='Y';")
			for row in self.cursor_stg.fetchall():
				exNews=ExNews()
				exNews.id=row[0]
				exNews.originId=row[1]
				exNews.providerId=row[2]
				exNews.isEnglish=row[3]
				exNews.title=row[4]
				yield exNews
		except Exception,e:
			print e
			self.log.error(e)

	def getById(self):
		pass

	def getByContentType(self,contentType):
		pass

	def update(self,exNews):
		pass
