# coding=utf-8
from com.process import *
from com.util.urlutil import *

class ManualHyperlinkProcess(HyperlinkProcess):
	"""
	Process manual English hyperlink
	Manual link format:<a href="" class="link_2" re="T" cate="manual_en_href">
	Sample:
		<a href="/law/content.php?content_type=T&origin_id=225627&provider_id=1&isEnglish=Y#i106" class="link_2" re="T"
		 cate="manual_en_href" >article 106</a>
	"""
	def __init__(self):
		super(ManualHyperlinkProcess,self).__init__()	
		self.manualPattern=re.compile(r'<a\s+href="(?P<linkurl>[^"]*)"\s+class="link_2"\s+re="T"\s+cate="manual_en_href"\s*>',re.I)
		self.oldHrefPattern=re.compile(r'o_href="[^"]*"',re.I)

	def search(self,content,start=0,posTupleList=[]):
		if content:
			tmpContent=content[start:]
			if tmpContent:
				matches=self.manualPattern.search(tmpContent)
				if matches and matches.group('linkurl'):
					posTuple=(start+matches.start(0),start+matches.end(0),matches.group('linkurl'))
					start+=matches.end(0)
					posTupleList.append(posTuple)
					self.search(content,start,posTupleList)
		return posTupleList

	def deleteCrossRefLink(self,article,targetArticle,provisionNum=0,attachmentId=0):
		if article and targetArticle:
			self.crossRefLinkDao.deleteBySrcDes(article.id,article.contentType,targetArticle.id,targetArticle.contentType,provisionNum,attachmentId)

	def removeAbandonedLink(self,article):
		if article:
			article.content=self.oldHrefPattern.sub('',article.content)
			return article
	 

	def pattern(self,article,posTupleList=[]):
		if article and posTupleList:
			for posTuple in posTupleList:
				if posTuple[2]:
					urlParamsMap=getUrlParams(posTuple[2])
					provisionNum=getUrlProvisionNum(posTuple[2])
					try:
						contentType,originId,providerId,isEnglish=oldUrlParamsMap['content_type'],oldUrlParamsMap['origin_id'],oldUrlParamsMap['provider_id'],oldUrlParamsMap['isEnglish']
						if not provisionNum:
							provisionNum=0
						keywordId=''
						targetArticle=self.getByOrigin(originId,providerId,isEnglish,contentType)
						if targetArticle:
							self.addCrossRefLink(article,targetArticle,keywordId,provisionNum)	
					except Exception,e:
						self.log.error(e)
		return article
