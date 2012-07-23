# coding=utf-8
from com.process import *
import re


class KeywordHyperlinkProcess(HyperlinkProcess):
	def __init__(self):
		super(KeywordHyperlinkProcess,self).__init__()	

	def search(self,content,start=0,posTupleList=[]):
		"""
		类似中文hyperlink的search,将文章中出现关键词的位置记录下来，并返回
		@param content 文章内容
		@start
		@posTupleList
		return 
		"""
		def checkNested():
			for item in posTupleList:
				if item[0]<=posTuple[0] and item[1]>=posTuple[1]:
					return True 
			return False
		lowerCaseContent=content.lower()#case inseneistive
		for keyword in self.keywordDao.getAll():
			keywordLen=len(keyword.content)	
			start=0
			while lowerCaseContent.find(keyword.content,start) != -1:
				startPos=lowerCaseContent.find(keyword.content,start)
				endPos=startPos+keywordLen
				matchStr=content[startPos:endPos]
				posTuple=(startPos,endPos,keyword.id,matchStr,keyword.fullTitleKeywordId)
				if not checkNested():
					posTupleList.append(posTuple)
				start=endPos
		posTupleList.sort(lambda posTuple1,posTuple2: - cmp(posTuple1[0],posTuple2[0]))#根据关键词出现的起始位置按降序排序
		return posTupleList

	def pattern(self,article,posTupleList=[]):
		"""
		从后向前,将出现关键字的地方加上超链接
		@param posTupleList 文章中出现关键字的信息列表
		@param article 当前处理的文章
		"""
		for posTuple in posTupleList:
			if self.checkTextShouldBeCited(article.content,posTuple[0],posTuple[1]):#if text should be cited
				if not  posTuple[4]:#if fullTitleKeywordId is not exist,means the keyword's type is 'F'
					lawCandidate=self.lawDao.getLawByKeywordId(posTuple[2])
				else:
					lawCandidate=self.lawDao.getLawByKeywordId(posTuple[4])
				if not lawCandidate:#如果没找到可加上hyperlink的法规
					continue
				if self.checkArticleInLawCandidate(article,lawCandidate):
					continue
				targetArticle=self.selectTargetArticle(article,lawCandidate)
				if targetArticle and  not article==targetArticle:#if current article and target article are not the same article
					targetArticleUrl=self.linkUrlFormat % (targetArticle.contentType,targetArticle.originId,targetArticle.providerId,targetArticle.isEnglish)
					rep=self.linkTagFormat % (targetArticleUrl,article.content[posTuple[0]:posTuple[1]])
					article.content=article.content[:posTuple[0]]+rep+article.content[posTuple[1]:]
					self.addCrossRefLink(article,targetArticle,posTuple[2])#添加hyperlink记录
		return article 

	def checkArticleInLawCandidate(self,article,lawCandidate):
		"""
		判断文章article是否在文章(法规)列表lawCandidate中
		"""
		if article and lawCandidate:
			for law in lawCandidate:
				if article.id==law.id and article.contentType==law.contentType:
					return True
		return False
		

if __name__=="__main__":
    process=KeywordHyperlinkProcess()
