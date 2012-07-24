# coding=utf-8
from com.process import *
from com.util.urlutil import *

class ManualHyperlinkProcess(HyperlinkProcess):
	"""
	Process manual English hyperlink
	Manual link format:<a href="" class="link_2_manual">
	Manual English hyperlink format:<a href="" class="link_2" re="T" cate="manual_en_href" target="_blank">
	Sample:
	<a href="/law/content.php?content_type=T&origin_id=225627&provider_id=1&isEnglish=Y#i106" class="link_2_manual" >article 106</a>
	Step 1:convert manual link format to manual English hyperlink format
	Step 2:find manual English hyperlink in content,and add corresponding record to cross_ref_link_en table
	"""
	def __init__(self):
		super(ManualHyperlinkProcess,self).__init__()	
		self.manualLinkPattern=re.compile(r'<a\s+href="(?P<linkurl>[^"]*)"[^>]*?cate="manual_en_href"[^>]*?>',re.I)

	def search(self,content,start=0,posTupleList=[]):
		if content:
			tmpContent=content[start:]
			if tmpContent:
				matches=self.manualLinkPattern.search(tmpContent)
				if matches and matches.group('linkurl'):
					posTuple=(start+matches.start(0),start+matches.end(0),matches.group('linkurl'))
					start+=matches.end(0)
					posTupleList.append(posTuple)
					self.search(content,start,posTupleList)
		return posTupleList

	def pattern(self,article,posTupleList=[]):
		if article and posTupleList:
			for posTuple in posTupleList:
				if posTuple[2]:
					urlParamsMap=getUrlParams(posTuple[2])
					provisionNum=getUrlProvisionNum(posTuple[2])
					try:
						contentType=urlParamsMap['content_type']
						originId=urlParamsMap['origin_id']
						providerId=urlParamsMap['provider_id']
						isEnglish=urlParamsMap['isEnglish']
						if not provisionNum:
							provisionNum=0
						keywordId=''
						targetArticle=self.getArticleByOrigin(originId,providerId,isEnglish,contentType)
						if targetArticle:
							self.addCrossRefLink(article,targetArticle,keywordId,provisionNum)	
					except Exception,e:
						self.log.error(e)
		return article

