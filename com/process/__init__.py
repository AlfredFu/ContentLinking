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
from com.dao.ExNewsSummaryDAO import *
from com.dao.ExNewsDAO import *
from com.entity.HyperlinkQueue import *
from com.entity.CrossRefLink import *
from com.entity.QueueItem import *
from com.process.filter import *
from com.process.rollback import backupArticle
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
		self.exNewsSummaryDao=ExNewsSummaryDAO.ExNewsSummaryDAO()
		self.exNewsDao=ExNewsDAO()
		self.log=getLog()    
		self.linkUrlFormat='/law/content.php?content_type=%s&origin_id=%s&provider_id=%s&isEnglish=%s'
		self.startLinkTagFormat='<a href="%s" class="link_2" re="T" cate="en_href" target="_blank" >'
		self.startLinkTagPattern=re.compile(r'<a href="(?P<hreflink>[^"^#]*?)#i(?P<proNum>[\d\.]*)"\s+class="link_2"\s+re="T"\s+cate="en_href"\s+target="_blank"\s*>',re.I)
		self.linkTagFormat=self.startLinkTagFormat+'%s</a>'

		#Following regex object (in which 'en_href' is an hyperlink mark) match English hyperlink tag 
		self.linkTagPattern=re.compile(r'<a\s+?[^>]*?cate=["\']en_href["\'][^>]*?>([^<]*?)</a>',re.I)
		
		#Following regex object match the text end with '([any text])'
		self.multiVerPat=re.compile(r'\([^)]*\)\s*$')

		#Following regex object match text end with string "of the people's republic of china"(ignore letter case and space)
		#In general,law title strip string "of the ...." is regarded as an abbreviation of law title
		self.abbrPat=re.compile(r'of the People\'s Republic of China\s*$',re.I)

		#Following regex object match pargraph which begin with Article * and end with 2 linefeed
		#Pargraph in article content matched is regarded as a provision
		self.provisionStartPattern=re.compile(r'(Article ([\d\.]+).?(.\n?)+?.?)(<br\s*/>[\r\s]*<br\s*/>)',re.I)

		#Following regex object match hidden provision position tag(both begin tag and end tag)
		self.provisionPosTagPattern=re.compile(r'<a name="(end_)?i[\d\.]+" re="T"></a>')
		
		#self.originManualLinkPattern=re.compile(r'(<a\s+href="[^"]*")[^>]*?class="link_2_manual"[^>]*(>)',re.I)	
		self.originManualLinkPattern=re.compile(r'(<a\s+)[^>]*?(href="[^"]*")[^>]*?class="link_2_manual"[^>]*(>)',re.I)	
		self.originManualLinkPatternEx=re.compile(r'(<a\s+)[^>]*?class="link_2_manual"[^>]*?(href="[^"]*")[^>]*(>)',re.I)	

		self.delManulLinkPattern=re.compile(r'<a[^>]*?class="link_2_del"[^>]*?>([^<]*?)</a\s*>',re.I)
	
		self.delTagPattern=re.compile(r'<span\s+cate=["\']link_2_del["\']\s*>[^<]*?</span>',re.I)
		self.delTagPatternStart=re.compile(r'<span\s+cate=["\']link_2_del["\']\s*>[^<]*$',re.I)
		self.delTagPatternEnd=re.compile(r'[^<]*?</span>',re.I)

	def eraseHyperlink(self,article):
		"""
		清除hyperlink所加的超链接
		hyperlink sample:<a href="" class="link_2" re="T" cate="en_href" target="_blank">Criminal Law</a>
		@param article 
		return 清除hyperlink链接后的文章
		"""	
		if article and article.content:
			article.content=self.delManulLinkPattern.sub(r'<span cate="link_2_del">\1</span>',article.content)
			article.content=self.originManualLinkPattern.sub(r'\1\2class="link_2" re="T" cate="manual_en_href" target="_blank"\3',article.content)
			article.content=self.originManualLinkPatternEx.sub(r'\1\2class="link_2" re="T" cate="manual_en_href" target="_blank"\3',article.content)
			article.content=self.linkTagPattern.sub(r'\1',article.content)

	def addProvisionPosTag(self,article):
		"""
		Mark provision position with following html tag(will not be displayed):
		Mark start position with:<a name="i2" re="T"></a>
		Mark end position with:<a name="end_i1" re="T"></a>
		@param article 
		"""	
		if article and article.content:
			article.content=self.provisionStartPattern.sub(r'<a name="i\2" re="T"></a>\1<a name="end_i\2" re="T"></a>\4',article.content)

	def removeProvisionPosTag(self,article):
		"""
		Remove provision position mark in content
		@param article 
		return 
		"""
		if article and article.content:
			article.content=self.provisionPosTagPattern.sub('',article.content)

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
		elif queueItem.contentType ==Article.CONTENT_TYPE_OVERVIEW_SUMMARY:
			article=self.exNewsSummaryDao.getById(queueItem.targetId)
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
		elif contentType ==Article.CONTENT_TYPE_OVERVIEW_SUMMARY:
			article=self.exNewsSummaryDao.getByOrigin(originId,providerId,isEnglish)
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
		elif article.contentType ==Article.CONTENT_TYPE_OVERVIEW_SUMMARY:
			self.exNewsSummaryDao.update(article)
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
			startMatch=re.search(r'<a[^>]+?>[^<]*$',content[:startPos])#在关键字出现位置前找锚标记a开始标签
			endMatch=re.search(r'[^<]*</a\s*>',content[endPos:])#在关键字出现位置后找锚标记结束符
			if startMatch and endMatch:
				return True
		return False

	def checkWrappedWithDelTag(self,content,startPos,endPos):
		"""
		检查startPos和endPos指定位置的关键词是否是手动删除的
		要求手动删除的连接是由<span cate="link_2_del">***</span>
		"""
		if content:
			startMatch=self.delTagPatternStart.search(content[:startPos])
			endMatch=self.delTagPatternEnd.search(content[endPos:])
			if startMatch and endMatch:
				return True
		return False	

	def checkBeginAndEndIsLetter(self,content,startPos,endPos):
		"""
		Check the first letters before startPos and the first letters after endPos in the content is English letters(include '_','-') or not
		return True when the first letter before startPos or the first letter after endPos is English letters
		otherwise return False	
		Sample:'Anti-trust Law' and  'Trust Law'
		"""
		try:
			fletter=content[startPos-1:startPos]#The first letter before startPos	
			lletter=content[endPos:endPos+1]#The first letter after endPos
			if (fletter and fletter in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_') or \
				(lletter and lletter in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'):
				return True
			else:
				return False
		except Exception,e:
			return False

	def checkTextShouldBeCited(self,content,startPos,endPos):
		"""
		判断内容content中startPos到endPos位置的文本是否应该加上超链接
		return True为加，False不加	
		"""
		if self.checkHyperlinkedKeyword(content,startPos,endPos) or self.checkWrappedWithDelTag(content,startPos,endPos) or self.checkBeginAndEndIsLetter(content,startPos,endPos):
			return False
		return True	

	def selectTargetArticle(self,article,articleCandidate):
		"""
		If target article has multiple version,
		Select one version article accroding to promulgation date and effect date,
		@param article hyperlink article
		@param lawCandidate candidate version 
		return one article in article candidate  
		"""
		#if len(articleCandidate) ==1:return articleCandidate[0]
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
			if str(article.proDate)<str(compDate):#发文日期在法规生效日期或法文日期之后，法规不能被引用
				continue
			elif str(latestDate) <str(compDate):
				latestDate=compDate
				latestArticle=targetArticle
		return latestArticle

	def deleteCrossRefLinkByArticleId(self,id,contentType):
		"""
		Delete corresponding hyperlink record by article id
		@param id article id
		"""
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
			self.queueDao.updateStatus(queueItem.targetId,queueItem.contentType,QueueItem.STATUS_PROCESSING)
	
	
	def addCrossRefLink(self,article,targetArticle,keywordId=0,itemId=0,attachmentId=0):
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
		self.queueDao.updateTargetArticleStatus(article.id,article.contentType)

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
			
		if title and title.find(' ')!=-1:
			keyword=self.keywordDao.findByContent(title)
			if not keyword:
				keyword=Keyword()
				keyword.content=title
				keyword.type=Keyword.KEYWORD_TYPE_FULL
				keywordId=self.keywordDao.add(keyword)	
				if self.abbrPat.search(title):
					abbrKeyword=Keyword()
					abbrKeyword.content=self.abbrPat.sub('',title)
					abbrKeyword.content=abbrKeyword.content.strip()
					if abbrKeyword.content.find(' ')!=-1:#single word will not be regard as a keyword
						abbrKeyword.type=Keyword.KEYWORD_TYPE_ABBR
						abbrKeyword.fullTitleKeywordId=keywordId
						self.keywordDao.add(abbrKeyword)
			else:
				keywordId=keyword.id
		else:
			keywordId=''
		return keywordId 
	
	def addProspectiveRevantArticleToQueue(self,article):
		"""
		If new legislation has been add to queue,prospective relevant article should be add to queue
		"""
		#self.queueDao.addAllToQueue()
		if article.title:
			abbrTitle=self.multiVerPat.sub('',article.title)
			abbrTitle=self.abbrPat.sub('',abbrTitle)
			abbrTitle=abbrTitle.strip()
			articleOriginTupleList=[]
			for row in self.lawDao.getArticleContainText(abbrTitle):
				articleOriginTupleList.append(row)
			for row in self.caseDao.getArticleContainText(abbrTitle):
				articleOriginTupleList.append(row)
			for row in self.exNewsDao.getArticleContainText(abbrTitle):
				articleOriginTupleList.append(row)
			for row in self.exNewsSummaryDao.getArticleContainText(abbrTitle):
				articleOriginTupleList.append(row)
			for row in self.newsletterDao.getArticleContainText(abbrTitle):
				articleOriginTupleList.append(row)
			for row in self.lncQADao.getArticleContainText(abbrTitle):
				articleOriginTupleList.append(row)
			for row in self.moduleQADao.getArticleContainText(abbrTitle):
				articleOriginTupleList.append(row)
			self.queueDao.addToQueue(articleOriginTupleList)
	
	def initial(self):
		"""
		Update keyword list and article list accroding to hyperlink queue		
		"""
		#Initial article status in hyperlink queue
		for queueItem in self.queueDao.getAll():
                        article=self.getArticle(queueItem)
                        #if new legislation has been add to queue
                        if article and article.actionType==Article.ACTION_TYPE_NEW and article.contentType==Article.CONTENT_TYPE_LAW:
                                self.addProspectiveRevantArticleToQueue(article)
                        elif article and article.actionType in [Article.ACTION_TYPE_UPDATE,Article.ACTION_TYPE_DELETE]:#
                                #update status and action_type of  relevant article
                                for item in self.crossRefLinkDao.getRelatedArticleId(queueItem.targetId,queueItem.contentType):
                                        self.queueDao.updateStatusActionType(item[0],item[1],Article.STATUS_AWAIT,Article.ACTION_TYPE_UPDATE)
				self.deleteCrossRefLinkByArticleId(queueItem.targetId,queueItem.contentType)#删除cross_ref_link表中的记录
		#Initial article content,keyword etc
		for queueItem in self.queueDao.getAll():
			article=self.getArticle(queueItem)
			if article:
				backupArticle(article)#backup article before it is processed
				if article.actionType in [Article.ACTION_TYPE_UPDATE,Article.ACTION_TYPE_DELETE]:#
					#do not switch the order of #sen1 and #sen2	
					if article.contentType==Article.CONTENT_TYPE_LAW:
						self.keywordDao.deleteByTarget(article.id,article.contentType)#sen1
					self.articleDao.deleteByTarget(article.id,article.contentType)#sen2
					if article.actionType==Article.ACTION_TYPE_UPDATE:
						self.removeProvisionPosTag(article)
						self.eraseHyperlink(article)
						
				if article.actionType in [Article.ACTION_TYPE_NEW,Article.ACTION_TYPE_UPDATE]:
					if article.contentType==Article.CONTENT_TYPE_LAW:			
						self.addProvisionPosTag(article)	
						keywordId=self.addKeyword(article.title)
						if keywordId:
							article.keywordId=keywordId
						else:
							article.keywordId=''
					else:
						article.keywordId=''
						
					self.articleDao.add(article)
				self.updateArticle(article)
			else:
				self.log.warning("no article with id:%s,type:%s found" %(queueItem.targetId,queueItem.contentType))
				#TODO remove queue item from hyperlink queue
		
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

