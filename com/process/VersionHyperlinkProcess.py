#coding=utf-8
from com.process import *
from com.dao.VersionDAO import *
from com.dao.ArticleDAO import *
from com.entity.Article import *
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
		判断文章标题是否符合多版本文章标题命名规范（标题中以'(****)'结尾）
		是返回True
		否返回False
		"""
		if article.title:
			if self.multiVerPat.search(article.title):
				return True
		return False

	def tripVersionInfo(self,title):
		"""
		文章标题中关于法规版本信息去掉
		return 去掉版本信息字符串后的标题
		"""
		if title:
			title=self.multiVerPat.sub('',title)
			title=title.lower()
			title=title.strip()
		return title
		
	def addVersionRelation(self,article):
		"""
		添加文章多版本参考信息
		"""
		keyword=self.keywordDao.findByContent(self.tripVersionInfo(article.title))
		if  keyword and keyword.id:
			refVersionArticleList=self.articleDao.findByKeywordId(keyword.id)
			versionList=[]
			for reVersionArticle in refVersionArticleList:
				if not article==reVersionArticle:
					versionSrc=Version()
					versionDes=Version()
					versionDes.desOriginId=versionSrc.srcOriginId=article.originId
					versionDes.desProviderId=versionSrc.srcProviderId=article.providerId
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
		self.versionDao.deleteByOrigin(article.originId,article.providerId,article.isEnglish)
		

	def process(self,article):
		if article.contentType==Article.CONTENT_TYPE_LAW:
			if article.actionType in [Article.ACTION_TYPE_UPDATE,Article.ACTION_TYPE_DELETE]:
				self.deleteVersionRelation(article)
			if article.actionType in [Article.ACTION_TYPE_UPDATE,Article.ACTION_TYPE_NEW]: 
				self.addVersionRelation(article)
		return article

if __name__=='__main__':
	process=VersionHyperlinkProcess()
	process.process()
