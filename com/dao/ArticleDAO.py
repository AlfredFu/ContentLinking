# coding=utf-8
from com.entity.Article import *
from com.dao import *

class ArticleDAO(DAO):
	def __init__(self):
		super(ArticleDAO,self).__init__()

	def updateContent(self):
		pass
	
	def updateTime(self):
		pass

	def findByKeywordId(self,keywordId=''):
		"""
		查询所有与指定关键词Id相关的文章
		"""
		try:
			self.curosr_hyperlink.execute("select article_id,content_type,origin_id,provider_id,isEnglish,target_id,action_type,status,keyword_id from article where keyword_id='%s'" % keywordId)
			articleList=[]
			for row in self.cursor_hyperlink.fetchall():
				article=Article()
				article.contentType=row[1]
				article.originId=row[2]
				article.providerId=row[3]
				article.isEnglish=row[4]
				article.id=row[5]
				articleList.append(article)
			return articleList
		except Exception,e:
			print e
			self.log.error(e)
				
	
