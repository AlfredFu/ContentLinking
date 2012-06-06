# coding=utf-8
from com.dao.LawDAO import *
from com.dao.CaseDAO import *
from com.dao.KeywordDAO import *
from com.dao.HyperlinkQueueDAO import *
import re


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

def deleteCrossRefLinkById(id):
	"根据文章id删除hyperlink记录"
	crossRefLinkDao=CrossRefLinkDAO()
	crossRefLinkDao.deleteBySrcId(id)
	crossRefLinkDao.deleteByDesId(id)

def updateTime(article):
	"更新文章时间戳，autonomy fetch有用，tax表为indbtime,case为in_time,请参考fetch配置"
	pass
	
def getArticle(id):
	"根据primary key获取文章"
	pass

def addRelatedArticleToQueue(taxid):
	"将相关文章加入到hyperlink队列"	
	pass
def update(article):
	"更新文章"
	pass

def main():
	for queueItem in queue:
		if queueItem.status !='N':
			if queueItem.contentType=='T':
				addRelatedArticleToQueue(queueItem.targetId)		
			deleteCrossRefLinkById(queueItem.targetId)#删除hyperlink关系记录
		
		article=getArticle(queueItem.targetId)
		article.content=eraseHyperlink(article.content)
		for keyword in keywordList:
			posTupleList=findKeywordPosInArticle(keyword,article)	
		article.content=patternContent(posTupleList,article.content)	
		
		update(article)	
		updateTime(article)

def findKeywordPosInArticle(keyword,article,start=0,posTupleList=[]):
	"类似中文hyperlink的search,将文章中出现关键词的位置记录下来，并返回"
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
	"从后向前"
	lawDao=LawDAO.LawDAO()
	for posTuple in posTupleList:
		if checkHyperlinkedKeyword(content,posTuple[0],posTuple[1]):#对加上超链接的关键字不做处理
			continue
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

def eraseHyperlink(content):
	"清除hyperlink所加的超链接"
	"hyperlink sample:<a href='' class='link_2' re='T' cate='en_href' >Criminal Law</a>"	
#	hyperlinkPattern=re.complie()
	content=re.sub(r'<a\s+href=\'[/\w\d\-\.]*\'\s+class=\'link_2\'\s+re=\'T\'\s+cate=\'en_href\'\s*>(.*)</a>',r'\1',content)
	return content

def checkHyperlinkedKeyword(content,startPos,endPos):
	"判断关键是是否被加上了超链接"
	if content:
		startMatch=re.search(r'<a.+?>\s*$',content[:startPos])
		endMatch=re.search(r'^</a\s*>',content[endPos:])
		if startMatch and endMatch:
			return True
	return False

def getProDate(targetId):
	"获取文章发文日期"
	pass

def selectLinkedVersion(article,versionCandidate):
	"对于多个版本的法规，需要根据发文日期和生效日期的信息选择一个"
	proDate=getProDate(article.id)
	
	for version in versionCandidate:
		if target:
			pass
		else:target=version

	return target		


def testEraseHyperlink():
	print eraseHyperlink("Welcome to <a href='#' class='link_2' re='T' cate='en_href_manual'>China</a> Hello <a href='/law/law-english-1-1245345.html' class='link_2' re='T' cate='en_href'>Fred's House</a> <a href='#'>hhhhhh<a>")

def testCheckHyperlinked():
	content="Welcome to <a href='#' class='link_2' re='T' cate='en_href_manual'>China</a>Hello<a href='/law/law-english-1-1245345.html' class='link_2' re='T' cate='en_href'>Fred's House</a> <a href='#'>hhhhhh<a>"
	startPos=re.search('China',content).start()
	endPos=re.search('China',content).end()
	startPos1=re.search('Hello',content).start()
	endPos1=re.search('Hello',content).end()
	print checkHyperlinkedKeyword(content,startPos,endPos)
	print checkHyperlinkedKeyword(content,startPos1,endPos1)
if __name__=="__main__":
	testEraseHyperlink()
	testCheckHyperlinked()
	#for keyword in keywordList:
		#print keyword.content	
	#for queueItem in queue:
		#print queueItem.originId,queueItem.providerId,queueItem.isEnglish
		#article=caseDao.getFullCaseByPrimaryKey(queueItem.originId,queueItem.providerId,queueItem.isEnglish)
		#for keyword in keywordList:
			#posTupleList=findKeywordPosInArticle(keyword,article)
			#print keyword.content,":",len(posTupleList)
			#print posTupleList
		#article.content=patternContent(posTupleList,article.content)
		#print article.content
		#contencaseDao.update(article)
		#print article
		#processKeywordHyperlink(keywordList,article)
