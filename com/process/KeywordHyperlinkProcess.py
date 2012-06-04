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
	posTupleList=[]
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

def findKeywordPosInArticle(keyword,article,start=0,posTupleList=[]):
	def checkNested():
		for item in posTupleList:
			if item[0]<=posTuple[0] and item[1]>=posTuple[1]:
				return True 
		return False
	lowerCaseContent=article.content.lower()#case inseneistive
	lowerKeywordContent=keyword.content.lower()
	while lowerCaseContent.find(lowerKeywordContent,start) != -1:
		startPos=lowerCaseContent.find(lowerKeywordContent,start)
		endPos=startPos+len(lowerKeywordContent)				
		posTuple=(startPos,endPos,keyword.id,keyword.content,keyword.fullTitleKeywordId)
		if not checkNested():
			posTupleList.append(posTuple)
		start=endPos
	
	posTupleList.reverse()
	return posTupleList

def patternContent(posTupleList,content,contentType='T'):
	lawDao=LawDAO.LawDAO()
	for posTuple in posTupleList:
		if not  posTuple[4]:
			targetArticle=lawDao.getLawByKeywordId(posTuple[2])
		else:
			targetArticle=lawDao.getLawByKeywordId(posTuple[4])
		if len(targetArticle) >1:
			#multiple version
			pass
		else:	
			rep="<a href='#' class='link_3' >"+content[posTuple[0]:posTuple[1]]+"<a>"
		content=content[0:posTuple[0]]+rep+content[posTuple[1]+1:]
	return content

def selectLinkedVersion(article,versionCandidate):
	
	pass
		

if __name__=="__main__":
	#for keyword in keywordList:
		#print keyword.content	
	for queueItem in queue:
		#print queueItem.originId,queueItem.providerId,queueItem.isEnglish
		article=caseDao.getFullCaseByPrimaryKey(queueItem.originId,queueItem.providerId,queueItem.isEnglish)
		for keyword in keywordList:
			posTupleList=findKeywordPosInArticle(keyword,article)
			#print keyword.content,":",len(posTupleList)
			#print posTupleList
		article.content=patternContent(posTupleList,article.content)
		print article.content
		caseDao.update(article)
		#print article
		#processKeywordHyperlink(keywordList,article)
