#coding=utf-8
from com.process import *
from com.dao.VersionDAO import *
import re

class VersionHyperlinkProcess(HyperlinkProcess):
	"""
	处理文章的多版本参考
	"""
	def __init__(self):
		super(VersionHyperlinkProcess,self).__init__()
		self.versionDao=VersionDAO()
	
	def checkMultipleVersion(self,article):
		"""
		判断文章标题是否符合多版本文章标题命名规范（标题中以'(Revised in ****)'结尾）
		是返回True
		否返回False
		"""
		if article.title:
			if re.search(r'\(revised in [0-9]{4}\)$',article.title,re.I):
				return True
		return False

	def addVersionRelation(self,article):
		"""
		添加文章多版本参考信息
		"""
		keyword=self.keywordDao.findByContent(article.title)
		if keyword.id:
			refVersionArticleList=self.articleDao.findByKeywordId(keyword.id)
			versionList=[]
			for reVersionArticle in refVersionArticleList:
				versionSrc=Version()
				versionDes=Version()
				versionDes.desOriginId=versionSrc.srcOriginId=article.originId
				versionDes.desOriginId=versionSrc.srcProviderId=article.providerId
				versionDes.desIsEnglish=versionSrc.srcIsEnglish=article.isEnglish
				versionDes.srcOriginId=versionSrc.desOriginId=reVersionArticle.originId
				versionDes.srcProviderId=versionSrc.desProviderId=reVersionArticle.providerId
				versionDes.srcIsEnglish=versionSrc.desIsEnglish=reVersionArticle.isEnglish
				versionList.append(versionSrc)
				versionList.append(versionDes)
			self.versionDao.addMany(versionList)
	
	def deleteVersionRelation(self,article):
		"""
		删除版本参照信息
		"""
		self.versionDao.deleteByOrigin(originId,providerId,isEnglish)
		
	def process(self):
		for queueItem in self.queueDao.getByType(Article.CONTENT_TYPE_TAX):
			article=self.getArticle(queueItem)
			if not self.checkMultipleVersion(article):continue
			if queueItem.actionType=='N':
				self.addVersionRelation(article)
			elif queueItem.actionType=='D':
				self.deleteVersionRelation(article)
			else:
				self.deleteVersionRelation(article)
				self.addVersionRelation(article)
				
if __name__=='__main__':
	print "test"
