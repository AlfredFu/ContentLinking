#!/usr/bin/env python
#coding=utf-8
from com.dao.HyperlinkQueueDAO import *
from com.dao.CaseDAO import * 
from com.dao.LawDAO import *
from com.dao.KeywordDAO import *
from com.entity.Keyword import *
from com.dao.ExNewsSummaryDAO import *
from com.dao.LncQADAO import *
from com.dao.ModuleQADAO import *
from com.dao.ProfNewsletterDAO import *
from com.dao.ArticleDAO import *
from com.dao.ExNewsDAO import *
import re

def initialQueue():
	"""
	初始化Hyperlink队列
	newlaw_stg.opr_load_status_en表
	"""
	caseDao=CaseDAO.CaseDAO()
	lawDao=LawDAO.LawDAO()
	hyperlinkQueueDao=HyperlinkQueueDAO.HyperlinkQueueDAO()
	keywordDao=KeywordDAO.KeywordDAO()
	exNewsSummaryDao=ExNewsSummaryDAO.ExNewsSummaryDAO()
	lncQADao=LncQADAO.LncQADAO()
	moduleQADao=ModuleQADAO.ModuleQADAO()
	profNewsletterDao=ProfNewsletterDAO.ProfNewsletterDAO()
	articleDao=ArticleDAO.ArticleDAO()
	exNewsDao=ExNewsDAO()

	def notInQueue(itemTuple):
		"""
		Check queueItem in table cross_ref_link_en
		If queueItem in table cross_ref_link_en return False,otherwise return True
		"""
		try:
			inqueueItem=hyperlinkQueueDao.getByTargetIdContentType(itemTuple[4],itemTuple[0],itemTuple[3])
			if inqueueItem:
				return False
			else:
				return True
		except Exception,e:
			return False

	actionType='N'
	status=1

	queueItemList=[]
	for case in caseDao.getAll():
		queueItemList.append((case.contentType,case.originId,case.providerId,case.isEnglish,case.id,actionType,status))

	for law in lawDao.getAll():
		queueItemList.append((law.contentType,law.originId,law.providerId,law.isEnglish,law.id,actionType,status))

	for news in exNewsDao.getAll():
		queueItemList.append((news.contentType,news.originId,news.providerId,news.isEnglish,news.id,actionType,status))

	for news in exNewsSummaryDao.getAll():
		queueItemList.append((news.contentType,news.originId,news.providerId,news.isEnglish,news.id,actionType,status))

	for news in lncQADao.getAll():
		queueItemList.append((news.contentType,news.originId,news.providerId,news.isEnglish,news.id,actionType,status))
	
	for news in profNewsletterDao.getAll():
		queueItemList.append((news.contentType,news.originId,news.providerId,news.isEnglish,news.id,actionType,status))

	for news in moduleQADao.getAll():
		queueItemList.append((news.contentType,news.originId,news.providerId,news.isEnglish,news.id,actionType,status))

	queueItemList=filter(notInQueue,queueItemList)
	hyperlinkQueueDao.addMany(queueItemList)

if __name__=="__main__":
	initialQueue()
