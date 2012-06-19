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
			lowerKeywordContent=keyword.content.lower()
			while lowerCaseContent.find(lowerKeywordContent,start) != -1:
				startPos=lowerCaseContent.find(lowerKeywordContent,start)
				endPos=startPos+len(lowerKeywordContent)				
				posTuple=(startPos,endPos,keyword.id,keyword.content,keyword.fullTitleKeywordId)
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
			if self.checkHyperlinkedKeyword(article.content,posTuple[0],posTuple[1]):#对已加上超链接的关键字不做处理
				continue
			if not  posTuple[4]:
				lawCandidate=self.lawDao.getLawByKeywordId(posTuple[2])
			else:
				lawCandidate=self.lawDao.getLawByKeywordId(posTuple[4])
			if not lawCandidate:#如果没找到可加上hyperlink的法规
				continue
				
			#print lawCandidate
			targetArticle=self.selectTargetArticle(article,lawCandidate)
			#targetLawUrl="/law/content.php?content_type=T&origin_id="+targetLaw.originId+"&provider_id="+targetLaw.providerId+"&isEnglish="+targetLaw.isEnglish
			targetArticleUrl="/law/content.php?content_type=%s&origin_id=%s&provider_id=%s&isEnglish=%s" % (targetArticle.contentType,targetArticle.originId,targetArticle.providerId,targetArticle.isEnglish)
			#rep="<a href='"+targetArticleUrl+"' class='link_3' >"+article.content[posTuple[0]:posTuple[1]]+"</a>"
			#rep="<a href='%s' class='link_2' re='T' cate='en_href' >%s</a>" % (targetArticleUrl,article.content[posTuple[0]:posTuple[1]])
			rep="<a href=\"%s\" class=\"link_2\" re=\"T\" cate=\"en_href\" >%s</a>" % (targetArticleUrl,article.content[posTuple[0]:posTuple[1]])
			article.content=article.content[:posTuple[0]]+rep+article.content[posTuple[1]:]
			self.addCrossRefLink(article,targetArticle,posTuple[2])#添加hyperlink记录
		#print article.content
		return article 

	"""
	def process(self,article=None):
		for queueItem in self.queueDao.getAll():
			self.updateOprLoadStatus(queueItem)
			article=self.getArticle(queueItem)	
			for keyword in self.keywordDao.getAll():
				posTupleList=self.search(keyword,article)
				
			article=self.pattern(posTupleList,article)
			self.updateArticle(article)
			print article.content

	def process(self,article):
		for keyword in self.keywordDao.getAll():
			posTupleList=self.search(keyword,article)
		article=self.pattern(posTupleList,article)
		#self.updateArticle(article)
		return article
		
	"""


if __name__=="__main__":
    process=KeywordHyperlinkProcess()
    process.process()
