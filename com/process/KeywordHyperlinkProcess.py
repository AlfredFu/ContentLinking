# coding=utf-8
import com.process.HyperlinkProcess
from com.dao.LawDAO import *
from com.dao.CaseDAO import *
from com.dao.KeywordDAO import *
from com.dao.HyperlinkQueueDAO import *
import re


class KeywordHyperlinkProcess(HyperlinkProcess):
	def __init__(self):
		super(KeywordHyperlinkProcess,self).__init__()	

	def findKeywordPosInArticle(keyword,article,start=0,posTupleList=[]):
		"""
		类似中文hyperlink的search,将文章中出现关键词的位置记录下来，并返回
		@param keyword 关键词对象
		@param article 文章对象
		@start
		@posTupleList
		return 
		"""
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

	def patternContent(posTupleList,article):
		"""
		从后向前,将出现关键字的地方加上超链接
		@param posTupleList 文章中出现关键字的信息列表
		@param article 当前处理的文章
		"""
		lawDao=LawDAO.LawDAO()
		for posTuple in posTupleList:
			if checkHyperlinkedKeyword(article.content,posTuple[0],posTuple[1]):#对加上超链接的关键字不做处理
				continue
			if not  posTuple[4]:
				lawCandidate=lawDao.getLawByKeywordId(posTuple[2])
			else:
				lawCandidate=lawDao.getLawByKeywordId(posTuple[4])
			if len(lawCandidate) >1:
				targetArticle=selectTargetLaw(article,lawCandidate)
			else:	
				targetArticle=lawCandidate[0]
		
			#targetLawUrl="/law/content.php?content_type=T&origin_id="+targetLaw.originId+"&provider_id="+targetLaw.providerId+"&isEnglish="+targetLaw.isEnglish
			targetArticleUrl="/law/content.php?content_type=%s&origin_id=%s&provider_id=%s&isEnglish=%s" % (targetArticle.contentType,targetArticle.originId,targetArticle.isEnglish)
			rep="<a href='"+targetArticleUrl+"' class='link_3' >"+article.content[posTuple[0]:posTuple[1]]+"<a>"
			article.content=article.content[0:posTuple[0]]+rep+article.content[posTuple[1]+1:]
		return article 





if __name__=="__main__":
	print "Hello world"
