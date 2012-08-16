#!/usr/bin/env python
#coding=utf-8
from com.dao.LawDAO import *
from com.dao.ArticleDAO import *
from com.dao.CaseDAO import *
from com.dao.KeywordDAO import *
from com.dao.HyperlinkQueueDAO import *
from com.dao.CrossRefLinkDAO import *
from com.dao.ProfNewsletterDAO import *
from com.dao.LncQADAO import *
from com.dao.ModuleQADAO import *
from com.dao.transferdao import *
from com.dao.ExNewsSummaryDAO import *
from com.dao.ExNewsDAO import *
from com.entity.Article import *
from com.entity.HyperlinkQueue import *
from com.entity.CrossRefLink import *
from com.entity.QueueItem import *

crossRefLinkDao=CrossRefLinkDAO.CrossRefLinkDAO()
lawDao=LawDAO.LawDAO()
articleDao=ArticleDAO.ArticleDAO()
caseDao=CaseDAO.CaseDAO()
keywordDao=KeywordDAO.KeywordDAO()
queueDao=HyperlinkQueueDAO.HyperlinkQueueDAO()
exNewsSummaryDao=ExNewsSummaryDAO.ExNewsSummaryDAO()
newsletterDao=ProfNewsletterDAO.ProfNewsletterDAO()
lncQADao=LncQADAO.LncQADAO()
moduleQADao=ModuleQADAO.ModuleQADAO()
transferDao=TransferDAO()
exNewsDao=ExNewsDAO()
log=getLog()    

def getArticle(queueItem):
	"""
	根据Hyperlink队列中的元素获取文章
	@param queueItem hyperlink队列中的一个元素
	return 返回文章
	"""
	if queueItem.contentType == Article.CONTENT_TYPE_LAW:
		article=lawDao.getById(queueItem.targetId)
	elif queueItem.contentType == Article.CONTENT_TYPE_CASE:
		article=caseDao.getById(queueItem.targetId)
	elif queueItem.contentType == Article.CONTENT_TYPE_NEWSLETTER:
		article=newsletterDao.getById(queueItem.targetId)
	elif queueItem.contentType == Article.CONTENT_TYPE_LNCQA:
		article=lncQADao.getById(queueItem.targetId)
	elif queueItem.contentType == Article.CONTENT_TYPE_MODULEQA:
		article=moduleQADao.getById(queueItem.targetId)
	elif queueItem.contentType ==Article.CONTENT_TYPE_OVERVIEW_SUMMARY:
		article=exNewsSummaryDao.getById(queueItem.targetId)
	else:
		article=exNewsDao.getById(queueItem.targetId)

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

def updateArticle(article,isTransfer=True):
	"""
	做完hyperlink后更新相关文章的时间
	"""
	if article.contentType == Article.CONTENT_TYPE_LAW:
		lawDao.update(article,isTransfer)
	elif article.contentType == Article.CONTENT_TYPE_CASE:
		caseDao.update(article,isTransfer)
	elif article.contentType == Article.CONTENT_TYPE_NEWSLETTER:
		newsletterDao.update(article,isTransfer)
	elif article.contentType == Article.CONTENT_TYPE_LNCQA:
		lncQADao.update(article,isTransfer)
	elif article.contentType == Article.CONTENT_TYPE_MODULEQA:
		moduleQADao.update(article,isTransfer)
	elif article.contentType ==Article.CONTENT_TYPE_OVERVIEW_SUMMARY:
		exNewsSummaryDao.update(article,isTransfer)
	else:
		exNewsDao.update(article,isTransfer)

def transferVersions():
	transferDao.cleanVersions()
	for version in transferDao.getAllVersions():
		transferDao.addVersion(version)

def transferCrossRefLink():
	transferDao.cleanCrossRefLinks()
	for crossRefLink in transferDao.getAllCrossRefLinks(): 
		transferDao.addCrossRefLink(crossRefLink)
	
def transferArticle():
	for queueItem in queueDao.getByStatus(Article.STATUS_WAIT_UPLOAD):
		article=getArticle(queueItem)
		if article:
			updateArticle(article)
			queueDao.updateStatus(queueItem.targetId,queueItem.contentType,Article.STATUS_FINISHED)

def transferData():
	transferVersions()
	transferCrossRefLink()
	transferArticle()

if __name__=="__main__":
	transferData()
