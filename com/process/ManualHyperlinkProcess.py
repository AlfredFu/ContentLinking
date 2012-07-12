# coding=utf-8
from com.process import *
from com.util.urlutil import *

class ManualHyperlinkProcess(HyperlinkProcess):
	def __init__(self):
		super(ManualHyperlinkProcess,self).__init__()	
		self.manualPattern=re.compile(r'<a href="(?P<linkurl>[^"]*)" class="link_2" re="T" cate="manual_en_href"\s*>',re.I)

	def search(self,content,start=0,posTupleList=[]):
		if content:
			tmpContent=content[start:]
			if tmpContent:
				matches=self.manualPattern.search(tmpContent)
				if matches and matches.group('linkurl'):
					posTuple=(start,start+matches.end(0),matches.group('linkurl'))
					start+=matches.end(0)
					posTupleList.append(posTuple)
					self.search(content,start,posTupleList)

	def pattern(self,article,posTupleList=[]):
		if article and posTupleList:
			for posTuple in posTupleList:
				urlParamsMap=getUrlParams(posTuple[2])
				provisionNum=getUrlProvisionNum(posTuple[2])
				if 'content_type' in urlParamsMap:
					contentType=urlParamsMap['content_type']
				else:
					contentType=''
				if 'origin_id' in urlParamsMap:
					originId=urlParamsMap['origin_id']
				else:
					originId=''
				if 'provider_id' in urlParamsMap:
					providerId=urlParamsMap['provider_id']
				else:
					providerId=''
				if 'isEnglish' in urlParamsMap:
					isEnglish=urlParamsMap['isEnglish']
				else:
					isEnglish=''
				if not provisionNum:
					provisionNum=0
				keywordId=''
				targetArticle=self.getByOrigin(originId,providerId,isEnglish,contentType)
				if targetArticle:
					self.addCrossRefLink(article,targetArticle,keywordId,provisionNum)	
