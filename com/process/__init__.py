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
from com.process.filter import *
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
		self.multiVerPat=re.compile(r'\(revised in [0-9]{4}\)\s*$',re.I)
		self.abbrPat=re.compile(r'of the People\'s Republic of China\s*$',re.I)

	def eraseHyperlink(self,article):
		"""
		清除hyperlink所加的超链接
		hyperlink sample:<a href='' class='link_2' re='T' cate='en_href'>Criminal Law</a>
		@param content 文章内容
		return 清除hyperlink链接后的文章内容
		"""	
		if article and article.content:
			article.content=re.sub(r'<a\s+?[^>]*?cate=["\']en_href["\']\s*>([^<]*?)</a>',r'\1',article.content)
			#content=re.sub(r'<a\s+href=[\'"][/\w\d\-\.]*?[\'"]\s+class=[\'"]link_2[\'"]\s+re=[\'"]T[\'"]\s+cate=[\'"]en_href[\'"]\s*>(.*?)</a>',r'\1',content)
			#content=re.sub(r'<a[^>]+?>([^<]*?)</a>','\\1',content)
			#contentcontent=re.sub(r'<?/?a>','',content)

	def addProvisionPosTag(self,article):
		"""
		Mark provision position with following html tag(will not be displayed):
		Mark start position with:<a name="i2" re="T"></a>
		Mark end position with:<a name="end_i1" re="T"></a>
		@param article 
		"""	
		if article and article.content:
			#provisionStartPattern=re.compile(r'(article ([\d\.]+)(.+\n?.+)+)(\n{1,})',re.I)
			#provisionStartPattern=re.compile(r'^(Article ([\d\.]+)(.+\n?.+)+)(\n{2})',re.MULTILINE)
			#provisionStartPattern=re.compile(r'(\n{2,})(article ([\d\.]+)(.+\n?.+)+)(\n{2,})',re.I)
			provisionStartPattern=re.compile(r'(Article ([\d\.]+).?(.\n?)+?.?)(\n\n|<br />\n?<br />)',re.I)#match pargraph which begin with Article * and end with 2 linefeed
			article.content=provisionStartPattern.sub(r'<a name="i\2" re="T"></a>\1<a name="end_i\2" re="T"></a>\4',article.content)
			#content=provisionStartPattern.sub(r'<a name="i\2" re="T"></a>\1<a name="end_i\2" re="T"></a>\4',content)	
			#content=provisionStartPattern.sub(r'\1<a name="i\3" re="T"></a>\2<a name="end_i\3" re="T"></a>\5',content)	

	def removeProvisionPosTag(self,article):
		"""
		Remove provision position mark in content
		@param article 
		return 
		"""
		if article and article.content:
			article.content=re.sub(r'<a name="(end_)?i[\d\.]+" re="T"></a>','',article.content)


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

		if article:
			article.actionType=queueItem.actionType
			article.status=queueItem.status	
			article.contentType=queueItem.contentType
			if article.content:
				article.content=article.content.replace('’','\'')
				article.content=article.content.replace('‘','\'')
				article.content=article.content.replace('”','"')
				article.content=article.content.replace('“','"')
			return article

	def getArticleByOrigin(self,originId,providerId,isEnglish='Y',contentType='T'):
		"""
		Get article by attribute origin_id ,provider_id and isEnglish
		"""
		if contentType == Article.CONTENT_TYPE_LAW:
			article=self.lawDao.getByOrigin(originId,providerId,isEnglish)
		elif contentType == Article.CONTENT_TYPE_CASE:
			article=self.caseDao.getByOrigin(originId,providerId,isEnglish)
		elif contentType == Article.CONTENT_TYPE_NEWSLETTER:
			article=self.newsletterDao.getByOrigin(originId,providerId,isEnglish)
		elif contentType == Article.CONTENT_TYPE_LNCQA:
			article=self.lncQADao.getByOrigin(originId,providerId,isEnglish)
		elif contentType == Article.CONTENT_TYPE_MODULEQA:
			article=self.moduleQADao.getByOrigin(originId,providerId,isEnglish)
		else:
			article=self.exNewsDao.getByOrigin(originId,providerId,isEnglish)
		if article:
			if article.contentType:
				article.contentType=contentType
			if article.content:
				article.content=article.content.replace('’','\'')
				article.content=article.content.replace('‘','\'')
				article.content=article.content.replace('”','"')
				article.content=article.content.replace('“','"')
			return article

	def updateArticle(self,article):
		"""
		做完hyperlink后更新相关文章的时间
		"""
		if article.contentType == Article.CONTENT_TYPE_LAW:
			self.lawDao.update(article)
		elif article.contentType == Article.CONTENT_TYPE_CASE:
			self.caseDao.update(article)
		elif article.contentType == Article.CONTENT_TYPE_NEWSLETTER:
			self.newsletterDao.update(article)
		elif article.contentType == Article.CONTENT_TYPE_LNCQA:
			self.lncQADao.update(article)
		elif article.contentType == Article.CONTENT_TYPE_MODULEQA:
			self.moduleQADao.update(article)
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
			targetLaw=self.lawDao.getById(targetArticle.targetId)
			if article.contentType==Article.CONTENT_TYPE_CASE:
				if targetLaw.proDate and targetLaw.effectDate:
					compDate=max([targetLaw.proDate,targetLaw.effectDate])#以发文日期和生效日期最近的一个作为比较日期
				elif targetLaw.proDate:
					compDate=targetLaw.proDate
				else:
					compDate=targetLaw.effectDate
			else:#其他内容类型发文日期作为比较日期
				compDate=targetLaw.proDate
			if article.proDate<compDate:continue#发文日期在法规生效日期或法文日期之后，法规不能被引用
			elif str(latestDate) <str(compDate):
				latestDate=compDate
				latestArticle=targetArticle
		return latestArticle

	def deleteCrossRefLinkByArticleId(self,id,contentType):
		"""
		Delete corresponding hyperlink record by article id
		@param id article id
		"""
		#self.crossRefLinkDao.deleteBySrcId(id,contentType)
		#self.crossRefLinkDao.deleteByDesId(id,contentType)
		#self.crossRefLinkDao.deleteByArticleIdContentType(id,contentType)
		#self.crossRefLinkDao.deleteByDesIdContentType(id,contentType)
		if id and contentType:
			self.crossRefLinkDao.deleteByArticleIdContentType(id,contentType)

	def updateRelatedArticleStatus(self,queueItem):
		"""
		Update related articles,set their status to STATUS_AWAIT
		"""
		for item in self.crossRefLinkDao.getRelatedArticleId(queueItem.targetId,queueItem.contentType):
			self.queueDao.updateStatus(item[0],item[1],Article.STATUS_AWAIT)

	def updateOprLoadStatus(self,queueItem):
		"""
		Update article status in hyperlink queue
		@param queueItem 
		"""
		if queueItem:
			"""
			if queueItem.actionType in [Article.ACTION_TYPE_DELETE,Article.ACTION_TYPE_UPDATE]:
				self.deleteCrossRefLinkByArticleId(queueItem.targetId,queueItem.contentType)#删除cross_ref_link表中的记录
			for item in self.crossRefLinkDao.getBySrcArticleIdContentType(queueItem.targetId,queueItem.contentType):#找出被当前文章引用的文章	
				self.queueDao.rollbackToStatus(item[0],item[1])#将status为STATUS_FINISHED改为STATUS_WAIT_UPLOAD
			for item in self.crossRefLinkDao.getByDesArticleIdContentType(queueItem.targetId,queueItem.contentType):#找出引用当前文章的文章
				self.queueDao.updateStatus(item[0],item[1],Article.STATUS_AWAIT)#将队列中的状态改为待处理
			if queueItem.contentType ==Article.CONTENT_TYPE_LAW and queueItem.actionType==Article.ACTION_TYPE_NEW:
				self.queueDao.updateActionType(queueItem.targetId,queueItem.contentType,Article.ACTION_TYPE_UPDATE)
				self.queueDao.addAllToQueue()
			"""	
			self.queueDao.updateStatus(queueItem.targetId,queueItem.contentType,QueueItem.STATUS_PROCESSING)
	
	
	def addCrossRefLink(self,article,targetArticle,keywordId='',itemId=0,attachmentId=0):
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

	def addKeyword(self,title):
		if title:
			title=self.multiVerPat.sub('',title)
			title=title.strip()#strip whitespace
			title=title.lower()#convert letters to lower case
			keyword=self.keywordDao.findByContent(title)
			if not keyword:
				keyword=Keyword()
				keyword.content=title
				keyword.type=Keyword.KEYWORD_TYPE_FULL
				keywordId=self.keywordDao.add(keyword)	
				"""
				if self.multiVerPat.search(article.title):
					multiVerKeyword.content=self.multiVerPat.sub('',article.title)
					multiVerKeyword.content=multiVerKeyword.content.strip()
					multiVerKeyword.content=multiVerKeyword.content.lower()
					multiVerKeyword.type=Keyword.KEYWORD_TYPE_ABBR
					multiVerKeyword.fullTitleKeywordId=keywordId
					keywordId=self.keywordDao.add(multiVerKeyword)
				"""
				if self.abbrPat.search(title):
					abbrKeyword=Keyword()
					abbrKeyword.content=self.abbrPat.sub('',title)
					abbrKeyword.content=abbrKeyword.content.strip()
					abbrKeyword.type=Keyword.KEYWORD_TYPE_ABBR
					abbrKeyword.fullTitleKeywordId=keywordId
					self.keywordDao.add(abbrKeyword)
			else:
				keywordId=keyword.id
			return keywordId 
	
	def initial(self):
		"""
		Update keyword list and article list accroding to hyperlink queue		
		"""
		for queueItem in self.queueDao.getAll():
			#debug code
			#begin
			if articleList and (queueItem.contentType,queueItem.originId,queueItem.providerId,queueItem.isEnglish) not in articleList:
				continue
			#print queueItem.targetId,' ',queueItem.contentType
			#end
			article=self.getArticle(queueItem)
			if not article:
				self.log.warning("no article with id:%s,type:%s found" %(queueItem.targetId,queueItem.contentType))
				continue
			if article.actionType in [Article.ACTION_TYPE_UPDATE,Article.ACTION_TYPE_DELETE]:#
				if article.contentType==Article.CONTENT_TYPE_LAW:
					self.keywordDao.deleteByTarget(article.id,article.contentType)
				self.articleDao.deleteByTarget(article.id,article.contentType)
				if article.actionType==Article.ACTION_TYPE_UPDATE:
					self.eraseHyperlink(article)
					self.removeProvisionPosTag(article)
				for item in self.crossRefLinkDao.getRelatedArticleId(queueItem.targetId,queueItem.contentType):#更新相关文章的状态	
					#self.queueDao.updateStatus(item[0],item[1],Article.STATUS_AWAIT)
					self.queueDao.updateStatusActionType(item[0],item[1],Article.STATUS_AWAIT,Article.ACTION_TYPE_UPDATE)
				self.deleteCrossRefLinkByArticleId(queueItem.targetId,queueItem.contentType)#删除cross_ref_link表中的记录
					
			if article.actionType in [Article.ACTION_TYPE_NEW,Article.ACTION_TYPE_UPDATE]:
				if article.contentType==Article.CONTENT_TYPE_LAW:			
					self.addProvisionPosTag(article)	
					keywordId=self.addKeyword(article.title)
					if article.actionType==Article.ACTION_TYPE_NEW:
						#TODO将所有文章加入到队列
						pass
				else:
					keywordId=''
				article.keywordId=keywordId
				self.articleDao.add(article)
			self.updateArticle(article)
		
	def begin(self,queueItem):
		"""
		Update queue items status and get article accroding queue item
		"""
		self.updateOprLoadStatus(queueItem)
		
	def process(self,article):
		if article:
			posTupleList=self.search(article.content)
			article=self.pattern(article,posTupleList)	
			del posTupleList[:]#清空list,否则会出现记录位置被重复使用的错误
			return article

	def end(self,queueItem):
		"""
		Update article status to STATUS_WAIT_UPLOAD in hyperlink queue
		"""
		self.queueDao.updateStatus(queueItem.targetId,queueItem.contentType,Article.STATUS_WAIT_UPLOAD)

if __name__=="__main__":
	process=HyperlinkProcess()	
	process.initial()
