# coding=utf-8
from com.dao.LawDAO import *
from com.dao.CaseDAO import *
from com.dao.KeywordDAO import *
from com.dao.HyperlinkQueueDAO import *
from com.dao.CrossRefLinkDAO import *
from com.dao.ExNewsDAO import *
from com.entity.HyperlinkQueue import *
from com.entity.CrossRefLink import *
from com.entity.QueueItem import *
import re

class HyperlinkProcess(object):
	def __init__(self):
		self.crossRefLinkDao=CrossRefLinkDAO.CrossRefLinkDAO()
		self.lawDao=LawDAO.LawDAO()
		self.caseDao=CaseDAO.CaseDAO()
		self.keywordDao=KeywordDAO.KeywordDAO()
		self.queueDao=HyperlinkQueueDAO.HyperlinkQueueDAO()
		self.exNewsDao=ExNewsDAO()
		self.log=getLog()    

	def eraseHyperlink(self,content):
		"""
		清除hyperlink所加的超链接
		hyperlink sample:<a href='' class='link_2' re='T' cate='en_href' >Criminal Law</a>
		@param content 文章内容
		return 清除hyperlink链接后的文章内容
		"""	
		content=re.sub(r'<a\s+href=\'[/\w\d\-\.]*?\'\s+class=\'link_2\'\s+re=\'T\'\s+cate=\'en_href\'\s*>(.*?)</a>',r'\1',content)
		#content=re.sub(r'<a.*?>','',content)
		#content=re.sub(r'<?/?a>','',content)
		return content
	
	def getArticle(self,queueItem):
		"""
		根据Hyperlink队列中的元素获取文章
		@param queueItem hyperlink队列中的一个元素
		return 返回文章
		"""
		if queueItem.contentType == Article.CONTENT_TYPE_LAW:
			article=self.lawDao.getById(queueItem.targetId)
		elif queueItem.contentType == Article.CONTENT_TYPE_CASE:
			article=self.caseDao.getById(queueItem.targetId)
		elif queueItem.contentType ==Article.CONTENT_TYPE_NEWS:
			article=self.exNewsDao.getById(queueItem.targetId)
		article.actionType=queueItem.actionType
		article.status=queueItem.status	
		return article

	def updateArticle(self,article):
		"""
		做完hyperlink后更新相关文章的时间
		"""
		if article.contentType==Article.CONTENT_TYPE_LAW:
			self.lawDao.update(article)
		elif article.contentType==Article.CONTENT_TYPE_CASE:
			self.caseDao.update(article)
		else:
			self.exNewsDao.update(article)

			
	def checkHyperlinkedKeyword(self,content,startPos,endPos):
		"""
		判断关键词是否被加上了超链接,是返回True,否则返回False
		@param content 
		@param startPos关键词在文章中的出现位置
		@param endPos 关键词结尾位置
		"""
		if content:
			startMatch=re.search(r'<a.+?>\s*$',content[:startPos])#在关键字出现位置前找锚标记a开始标签
			endMatch=re.search(r'^</a\s*>',content[endPos:])#在关键字出现位置后找锚标记结束符
			if startMatch and endMatch:
				return True
		return False

	def selectTargetArticle(self,article,articleCandidate):
		"""
		对于多个版本的文章(法规)，需要根据发文日期和生效日期的信息选择一个
		@param article hyperlink文章，
		@param lawCandidate多版本文章(法规)列表
		return 返回文章(文章)对象
		"""
		if len(articleCandidate) ==1:return articleCandidate[0]
		latestDate=''
		latestArticle=None
		for targetArticle in articleCandidate:
			if article.contentType=='C':#法规以发文日期作为比较日期
				compDate=max([targetArticle.proDate,targetArticle.effectDate])#其他内容类型以发文日期和生效日期最近的一个作为比较日期
			else:
				compDate=targetArticle.prodate
					
			if article.proDate<compDate:continue#发文日期在法规生效日期或法文日期之后，法规不能被引用
			elif latestDate <compDate:
				latestDate=compDate
				latestArticle=targetArticle
		return latestArticle


	def deleteCrossRefLinkByArticleId(self,id):
		"根据文章id删除hyperlink记录"
		self.crossRefLinkDao.deleteBySrcId(id)
		self.crossRefLinkDao.deleteByDesId(id)

	def updateRelatedArticleActionType(self,queueItem):
		"""
		将相关文章的相关文章action_type属性改为U
		"""
		for item in self.crossRefLinkDao.getRelatedArticleId(queueItem.targetId):
			self.queueDao.updateActionType('U',item[0])

	def updateOprLoadStatus(self,queueItem):
		"""
		更新队列中文章的状态
		"""
		if queueItem.contentType =='T':
			if queueItem.actionType in ['D','U']:
				self.updateRelatedArticleActionType(queueItem)#找出相关文章，更新相关文章的在hyperlink队列中的状态为U
			elif article.actionType=='N':
				self.queueDao.addAllToQueue()#更新队列中状态为空的数据状态为U
		if queueItem.actionType in ['D','U']:
			self.deleteCrossRefLinkByArticleId(queueItem.targetId)#删除cross_ref_link表中的记录
			#TODO处理被引用的文章
		self.queueDao.updateStatus(queueItem.targetId,QueueItem.STATUS_PROCESSING,queueItem.contentType)
	
	def addCrossRefLink(self,article,targetArticle,keywordId='',itemId='',attachmentId=''):
		"""
		add record to cross_ref_link
		"""
		crossRefLink=CrossRefLink()
		crossRefLink.srcArticleId=article.id
		crossRefLink.srcContentType=article.contentType
		crossRefLink.srcOriginId=article.originId
		crossRefLink.srcProviderId=article.providerId
		crossRefLink.srcIsEnglish=article.isEnglish
		crossRefLink.desArticleId=targetArticle.id
		crossRefLink.desContentType=targetArticle.contentType
		crossRefLink.desOriginId=targetArticle.originId
		crossRefLink.desProviderId=targetArticle.providerId
		crossRefLink.desIsEnglish=targetArticle.isEnglish		
		crossRefLink.desAttachmentId=attachmentId

		crossRefLink.keywordId=keywordId
		crossRefLink.desItemId=itemId
		
		self.crossRefLinkDao.add(crossRefLink)

	def process(self,article):
		pass	
