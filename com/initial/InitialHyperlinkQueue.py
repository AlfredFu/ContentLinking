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
	exNewsDao=ExNewsDAO()

	actionType='N'
	status=1

	queueItemList=[]
	for case in caseDao.getAll():
		queueItemList.append((case.contentType,case.originId,case.providerId,case.isEnglish,case.id,actionType,status))

	p=re.compile(r'\(revised in [0-9]{4}\)$',re.I)
	ss=re.compile(r'of the People\'s Republic of China',re.I)
	for law in lawDao.getAll():
		queueItemList.append((law.contentType,law.originId,law.providerId,law.isEnglish,law.id,actionType,status))
		
		if law.title:
			keyword=Keyword()
			keyword.content=p.sub('',law.title)
			keyword.type=Keyword.KEYWORD_TYPE_FULL
			keyword.fullTitleKeywordId=''
			keywordId=keywordDao.add(keyword)

			if ss.search(keyword.content):
				abbrKeyword=Keyword()
				abbrKeyword.content=ss.sub('',keyword.content)	 
				abbrKeyword.type=Keyword.KEYWORD_TYPE_ABBR
				abbrKeyword.fullTitleKeywordId=keywordId
				keywordDao.add(abbrKeyword)


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
	hyperlinkQueueDao.addMany(queueItemList)

if __name__=="__main__":
	initialQueue()
