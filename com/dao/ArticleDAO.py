# coding=utf-8
from com.entity.Article import *
from com.dao import *

class ArticleDAO(DAO):
	"""
	操作article_en表
	"""
	tableName='article_en'
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
			self.cursor_hyperlink.execute("select article_id,content_type,origin_id,provider_id,isEnglish,target_id,action_type,status,keyword_id from "+ArticleDAO.tableName+" where keyword_id='%s'" % keywordId)
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
			self.log.error(e)
				
	def addMany(self,articleTupleList):
		"""
		批量添加article
		"""
		try:
			for articleTuple in articleTupleList:
				#print "replace into "+ArticleDAO.tableName+"(content_type,origin_id,provider_id,isEnglish,target_id,action_type,status,keyword_id) values('%s','%s',%s,'%s',%s,'%s','%s',%s)" % articleTuple
				self.cursor_hyperlink.execute("replace into "+ArticleDAO.tableName+"(content_type,origin_id,provider_id,isEnglish,target_id,action_type,status,keyword_id) values('%s','%s',%s,'%s',%s,'%s','%s','%s')" % articleTuple)
				
			self.conn_hyperlink.commit()
		except Exception,e:
			self.log.error(e)	

	def add(self,article):
		try:
			if article.keywordId:
				sql="REPLACE INTO "+ArticleDAO.tableName+"(content_type,origin_id,provider_id,isEnglish,target_id,action_type,status,keyword_id) values('%s','%s',%s,'%s',%s,'%s','%s',%s)" % (article.contentType,article.originId,article.providerId,article.isEnglish,article.id,article.actionType,article.status,article.keywordId)
			else:
				sql="REPLACE INTO "+ArticleDAO.tableName+"(content_type,origin_id,provider_id,isEnglish,target_id,action_type,status) values('%s','%s',%s,'%s',%s,'%s','%s')" % (article.contentType,article.originId,article.providerId,article.isEnglish,article.id,article.actionType,article.status)
				
			self.cursor_hyperlink.execute(sql)
			self.conn_hyperlink.commit()	
		except Exception,e:
			self.log.error(e)
	
	def deleteByOrigin(self,originId,providerId,isEnglish,contentType):
		if originId and providerId and isEnglish and contentType:
			sql="delete from article_en where origin_id='%s' and provider_id=%s and isEnglish='%s' and content_type='%s';" %(originId,providerId,isEnglish,contentType)
			try:
				self.cursor_hyperlink.execute(sql)
				self.conn_hyperlink.commit()
			except Exception,e:
				self.log.error(e)

	def deleteByTarget(self,targetId,contentType):
		if targetId and contentType:
			sql="delete from article_en where target_id=%s and content_type='%s';" %(targetId,contentType)
			try:
				self.cursor_hyperlink.execute(sql)
				self.conn_hyperlink.commit()
			except Exception,e:
				self.log.error(e)
