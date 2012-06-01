from com.dao.LawDAO import *
from com.dao.CaseDAO import *
from com.dao.KeywordDAO import *
from com.dao.HyperlinkQueueDAO import *


keywordDao=KeywordDAO.KeywordDAO()
queueDao=HyperlinkQueueDAO()
keywordList=keywordDao.getAll()
queue=queueDao.getAll()
caseDao=CaseDAO.CaseDAO()
def processKeywordHyperlink(keywordList,article):
	global caseDao
	hyperlinkPattern=""
	lawDao=LawDAO.LawDAO()
	for keyword in keywordList: 
		if article.content.find(keyword.content) != -1:
			keywordLawTupleList=lawDao.getLawByKeywordId(keyword.id)
			#print keywordLawTupleList
			linkUrl="/law/law-english-%s-%s.html" % (keywordLawTupleList[0][1],keywordLawTupleList[0][0]);	
			#hyperlinkText="<a class=\'link_2\' re=\'T\' target=\'_blank\' href=\'%s\'>%s</a>" %(linkUrl,keyword.content)
			hyperlinkText="<a class=link_2 re=T target=_blank href=%s>%s</a>" %(linkUrl,keyword.content)
			article.content=article.content.replace(keyword.content,hyperlinkText)
			caseDao.update(article)
			#TODO cross_ref_link

if __name__=="__main__":
	for queueItem in queue:
		#print queueItem.originId,queueItem.providerId,queueItem.isEnglish
		article=caseDao.getFullCaseByPrimaryKey(queueItem.originId,queueItem.providerId,queueItem.isEnglish)
		#print article
		processKeywordHyperlink(keywordList,article)
