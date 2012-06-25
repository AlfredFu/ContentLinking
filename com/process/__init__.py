# coding=utf-8
from com.dao.LawDAO import *
from com.dao.ArticleDAO import *
from com.dao.CaseDAO import *
from com.dao.KeywordDAO import *
from com.dao.HyperlinkQueueDAO import *
from com.dao.CrossRefLinkDAO import *
from com.dao.ProfNewsletterDAO import *
from com.dao.LncQADAO import *
from com.dao.ModuleQADAO import *
from com.dao.ExNewsDAO import *
from com.entity.HyperlinkQueue import *
from com.entity.CrossRefLink import *
from com.entity.QueueItem import *
import re

class HyperlinkProcess(object):
	def __init__(self):
		self.crossRefLinkDao=CrossRefLinkDAO.CrossRefLinkDAO()
		self.lawDao=LawDAO.LawDAO()
		self.articleDao=ArticleDAO.ArticleDAO()
		self.caseDao=CaseDAO.CaseDAO()
		self.keywordDao=KeywordDAO.KeywordDAO()
		self.queueDao=HyperlinkQueueDAO.HyperlinkQueueDAO()
		self.newsletterDao=ProfNewsletterDAO.ProfNewsletterDAO()
		self.lncQADao=LncQADAO.LncQADAO()
		self.moduleQADao=ModuleQADAO.ModuleQADAO()
		self.exNewsDao=ExNewsDAO()
		self.log=getLog()    
		self.hyperlinkPatternStr=r'<a href="[^"]*" class="link_2" re="T" cate="en_href" >'

	def eraseHyperlink(self,content):
		"""
		清除hyperlink所加的超链接
		hyperlink sample:<a href='' class='link_2' re='T' cate='en_href'>Criminal Law</a>
		@param content 文章内容
		return 清除hyperlink链接后的文章内容
		"""	
		content=re.sub(r'<a\s+?[^>]*?cate=["\']en_href["\']\s*>([^<]*?)</a>',r'\1',content)
		#content=re.sub(r'<a\s+href=[\'"][/\w\d\-\.]*?[\'"]\s+class=[\'"]link_2[\'"]\s+re=[\'"]T[\'"]\s+cate=[\'"]en_href[\'"]\s*>(.*?)</a>',r'\1',content)
		#content=re.sub(r'<a[^>]+?>([^<]*?)</a>','\\1',content)
		#contentcontent=re.sub(r'<?/?a>','',content)
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
		elif queueItem.contentType == Article.CONTENT_TYPE_NEWSLETTER:
			article=self.newsletterDao.getById(queueItem.targetId)
		elif queueItem.contentType == Article.CONTENT_TYPE_LNCQA:
			article=self.lncQADao.getById(queueItem.targetId)
		elif queueItem.contentType == Article.CONTENT_TYPE_MODULEQA:
			article=self.moduleQADao.getById(queueItem.targetId)
		else:
			article=self.exNewsDao.getById(queueItem.targetId)

		if article and article.content:
			article.actionType=queueItem.actionType
			article.status=queueItem.status	
			article.content=article.content.replace('’','\'')
			article.content=article.content.replace('‘','\'')
			article.content=article.content.replace('”','"')
			article.content=article.content.replace('“','"')
			return article

	def getArticleByOrigin(self,originId,providerId,isEnglish='Y',contentType='T'):
		"""
		Get article by attribute origin_id ,provider_id and isEnglish
		"""
		if queueItem.contentType == Article.CONTENT_TYPE_LAW:
			article=self.lawDao.getByOrigin(originId,providerId,isEnglish)
		elif queueItem.contentType == Article.CONTENT_TYPE_CASE:
			article=self.caseDao.getByOrigin(originId,providerId,isEnglish)
		elif queueItem.contentType == Article.CONTENT_TYPE_NEWSLETTER:
			article=self.newsletterDao.getByOrigin(originId,providerId,isEnglish)
		elif queueItem.contentType == Article.CONTENT_TYPE_LNCQA:
			article=self.lncQADao.getByOrigin(originId,providerId,isEnglish)
		elif queueItem.contentType == Article.CONTENT_TYPE_MODULEQA:
			article=self.moduleQADao.getByOrigin(originId,providerId,isEnglish)
		else:
			article=self.exNewsDao.getByOrigin(originId,providerId,isEnglish)
		if article and article.content:
			article.actionType=queueItem.actionType
			article.status=queueItem.status	
			article.content=article.content.replace('’','\'')
			article.content=article.content.replace('‘','\'')
			article.content=article.content.replace('”','"')
			article.content=article.content.replace('“','"')
			return article

	def updateArticle(self,article):
		"""
		做完hyperlink后更新相关文章的时间
		"""
		if queueItem.contentType == Article.CONTENT_TYPE_LAW:
			article=self.lawDao.update(article)
		elif queueItem.contentType == Article.CONTENT_TYPE_CASE:
			article=self.caseDao.update(article)
		elif queueItem.contentType == Article.CONTENT_TYPE_NEWSLETTER:
			article=self.newsletterDao.update(article)
		elif queueItem.contentType == Article.CONTENT_TYPE_LNCQA:
			article=self.lncQADao.update(article)
		elif queueItem.contentType == Article.CONTENT_TYPE_MODULEQA:
			article=self.moduleQADao.update(article)
		else:
			article=self.exNewsDao.update(article)

			
	def checkHyperlinkedKeyword(self,content,startPos,endPos):
		"""
		判断关键词是否被加上了超链接,是返回True,否则返回False
		@param content 
		@param startPos关键词在文章中的出现位置
		@param endPos 关键词结尾位置
		"""
		if content:
			#startMatch=re.search(r'<a.+?>\s*$',content[:startPos])#在关键字出现位置前找锚标记a开始标签
			startMatch=re.search(r'<a[^>]+?>\s*$',content[:startPos])#在关键字出现位置前找锚标记a开始标签
			endMatch=re.search(r'^</a\s*>',content[endPos:])#在关键字出现位置后找锚标记结束符
			if startMatch and endMatch:
				return True
		return False

	def selectTargetArticle(self,article,articleCandidate):
		"""
		If target article has multiple version,
		Select one version article accroding to promulgation date and effect date,
		@param article hyperlink article
		@param lawCandidate candidate version 
		return one article in article candidate  
		"""
		if len(articleCandidate) ==1:return articleCandidate[0]
		latestDate=''
		latestArticle=None
		for targetArticle in articleCandidate:
			if article.contentType==Article.CONTENT_TYPE_CASE:#法规以发文日期作为比较日期
				compDate=max([targetArticle.proDate,targetArticle.effectDate])#其他内容类型以发文日期和生效日期最近的一个作为比较日期
			else:
				compDate=targetArticle.prodate
					
			if article.proDate<compDate:continue#发文日期在法规生效日期或法文日期之后，法规不能被引用
			elif latestDate <compDate:
				latestDate=compDate
				latestArticle=targetArticle
		return latestArticle

	def deleteCrossRefLinkByArticleId(self,id):
		"""
		Delete corresponding hyperlink record by article id
		@param id article id
		"""
		self.crossRefLinkDao.deleteBySrcId(id)
		self.crossRefLinkDao.deleteByDesId(id)

	def updateRelatedArticleStatus(self,queueItem):
		"""
		将相关文章的相关文章action_type属性改为U
		"""
		for item in self.crossRefLinkDao.getRelatedArticle(queueItem.targetId,queueItem.contentType):
			self.queueDao.updateStatus(item[0],item[1],Article.STATUS_AWAIT)

	def updateOprLoadStatus(self,queueItem):
		"""
		Update article status in hyperlink queue
		@param queueItem 
		"""
		if queueItem.contentType ==Article.CONTENT_TYPE_LAW:
			if queueItem.actionType in [Article.ACTION_TYPE_DELETE,Article.ACTION_TYPE_UPDATE]:
				self.updateRelatedArticleStatus(queueItem)#找出相关文章，更新相关文章的在hyperlink队列中的状态为U
			elif queueItem.actionType==Article.ACTION_TYPE_NEW:
				self.queueDao.addAllToQueue()#更新队列中状态为空的数据状态为U
		if queueItem.actionType in [Article.ACTION_TYPE_DELETE,Article.ACTION_TYPE_UPDATE]:
			self.deleteCrossRefLinkByArticleId(queueItem.targetId)#删除cross_ref_link表中的记录
		self.queueDao.updateStatus(queueItem.targetId,queueItem.contentType,QueueItem.STATUS_PROCESSING)
	
	
	def addCrossRefLink(self,article,targetArticle,keywordId='',itemId='',attachmentId=''):
		"""
		Add record to cross_ref_link
		@param article the article which has link to another article 
		@param targetArticle 
		@param keywordId
		@param itemId provision sequence number
		@param attachmentId
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

	def search(self,content,start=0,posTupleList=[]):
		"""
		To be implemented in subclass	
		@param content 
		"""
		pass

	def pattern(self,article,posTupleList=[]):
		"""
		To be implemented in subclass	
		@param article 
		"""
		pass

	def begin(self,queueItem):
		"""
		"""
		self.updateOprLoadStatus(queueItem)
		article=self.getArticle(queueItem)
		keywordId=''
		if article: 
			if article.contentType==Article.CONTENT_TYPE_LAW:
				keyword=Keyword()
				keyword.content=re.sub(r'\(revised in [0-9]{4}\)$','',article.title)
				keyword.type=Keyword.KEYWORD_TYPE_FULL
				keywordId=self.keywordDao.add(keyword)	
				if re.search(r'of the People\'s Republic of China',keyword.content):
					abbrKeyword=Keyword()
					abbrKeyword.content=re.sub(r'of the People\'s Republic of China','',keyword.content,flags=re.I)
					abbrKeyword.type=Keyword.KEYWORD_TYPE_ABBR
					abbrKeyword.fullTitleKeywordId=keywordId
					self.keywordDao.add(abbrKeyword)
			article.keywordId=keywordId
			self.articleDao.add(article)
		
			

	def process(self,article):
		self.log.info("Processing article id:%s,content type:%s" %(article.id,article.contentType))
		posTupleList=self.search(article.content)
		article=self.pattern(article,posTupleList)	
		return article

	def end(self,queueItem):
		"""
		Update article status to STATUS_WAIT_UPLOAD in hyperlink queue
		"""
		self.queueDao.updateStatus(queueItem.targetId,queueItem.contentType,Article.STATUS_WAIT_UPLOAD)
