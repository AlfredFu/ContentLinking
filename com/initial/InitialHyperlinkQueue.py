#coding=utf-8
from com.dao.HyperlinkQueueDAO import *
from com.dao.CaseDAO import * 
from com.dao.LawDAO import *
from com.dao.ExNewsDAO import *
"""
初始化Hyperlink队列
newlaw_stg.opr_load_status_en表
"""
caseDao=CaseDAO()
lawDao=LawDAO()
exNewsDao=ExNewsDAO()
hyperlinkQueueDao=HyperlinkQueueDAO.HyperlinkQueueDAO()

actionType='N'
status=1

queueItemList=[]
for case in caseDao.getAll():
	queueItemList.append((case.contentType,case.originId,case.providerId,case.isEnglish,case.id,actionType,status))

for law in lawDao.getAll():
	queueItemList.append((law.contentType,law.originId,law.providerId,law.isEnglish,law.id,actionType,status))

for news in exNewsDao.getAll():
	queueItemList.append(news.contentType,news.originId,news.providerId,news.isEnglish,news.id,actionType,status))

hyperlinkQueueDao.addMany(queueItemList)
