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
		self.versionDao=VersionDAO.VersionDAO()
		self.articleDao=ArticleDAO()
	
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

	def tripVersionInfo(self,title):
		"""
		文章标题中关于法规版本信息去掉
		return 去掉版本信息字符串后的标题
		"""
		if title:
			p=re.compile(r'\(revised in [0-9]{4}\)$',re.I)
			title=p.sub('',title)
		return title
		
	def addVersionRelation(self,article):
		"""
		添加文章多版本参考信息
		"""
		keyword=self.keywordDao.findByContent(self.tripVersionInfo(article.title))
		if keyword.id:
			refVersionArticleList=self.articleDao.findByKeywordId(keyword.id)
			versionList=[]
			for reVersionArticle in refVersionArticleList:
				if (article.originId,article.providerId,article.isEnglish) != (reVersionArticle.originId,reVersionArticle.providerId,reVersionArticle.isEnglish):
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
		self.versionDao.deleteByOrigin(originId,providerId,isEnglish)
		
	def process(self):
		for queueItem in self.queueDao.getByContentType(Article.CONTENT_TYPE_LAW):
			article=self.getArticle(queueItem)
			#if not self.checkMultipleVersion(article):continue
			if queueItem.actionType==QueueItem.ACTION_TYPE_NEW:
				self.addVersionRelation(article)
			elif queueItem.actionType==QueueItem.ACTION_TYPE_UPDATE:
				self.deleteVersionRelation(article)
			else:
				self.deleteVersionRelation(article)
				self.addVersionRelation(article)
				
if __name__=='__main__':
	process=VersionHyperlinkProcess()
	process.process()
	#print process.tripVersionInfo("Company Law of the People's Republic of China (Revised in 1999)")
