# coding=utf-8
from com.process import *
import re

class ProvisionHyperlinkProcess(HyperlinkProcess):
	"""
	法条hyperlink
	"""
	def __init__(self):
		super(ProvisionHyperlinkProcess,self).__init__()
		#self.provisionPatternStr=r"(?P<astr>article\s+(?P<articleNum>\d+\.?\d+))\s+of\s+the\s+(<a href=\"(?P<href>[^\"^>]*?)\" class=\"link_2\" re=\"T\" cate=\"en_href\"\s*>).+?</a>"
		self.provisionPatternStr=r'(?P<astr>article\s+(?P<articleNum>[\d+\.]+?))\s+of\s+the [\s"]*?(<a href="(?P<href>[^\"^>]*?)" class="link_2" re="T" cate="en_href"\s*>)(?P<keyword>.+?)</a>'
		self.provisionPattern=re.compile(self.provisionPatternStr,re.I)

	def addProvisionPosTag(self,content):
		"""
		给法条添加上位置标记
		开始标记<a name="i2" re="T"></a>
		结束标记<a name="end_a148318_att-1_i1" re="T"></a>
		"""	
		provisionStartPattern=re.compile(r'(article ([\d\.]+)(.+\n?.+)+)(\n{2,})',re.I)
		content=provisionStartPattern.sub(r'<a name="i\2" re="T"></a>\1<a name="end_i\2" re="T"></a>\4',content)	
		#provisionStartPattern=re.compile(r'(\n{2,})(article ([\d\.]+)(.+\n?.+)+)(\n{2,})',re.I)
		#content=provisionStartPattern.sub(r'\1<a name="i\3" re="T"></a>\2<a name="end_i\3" re="T"></a>\5',content)	
		return content

	def removeProvisionPosTag(self,content):
		"""
		移除法条位置标记
		"""
		return re.sub(r'<a name="(end_)?i[\d\.]+" re="T"></a>','',content)

	def checkProvisionExist(self,originId,providerId,isEnglish='Y',contentType='T',itemId):
		"""
		判断法条在文章中是否存在(只在已加法条位置标记后有效)
		存在返回True,否则返回false(如果在找到多个也返回false,避免hyperlink错误)
		"""
		article=self.getArticleByOrigin(originId,providerId,isEnglish,contentType)
		if article:
			if article.content.count('<a name="i%s" re="T"></a>' % itemId)==1:
				return True
		return False
	
	def search(self,content,start=0,posTupleList=[]):
		tmpContent=content[start:]
		if tmpContent:
			matches=self.provisionPattern.search(tmpContent)	
			if matches:
				startPos=start+matches.start(1)
				endPos=start+matches.end(1)
				href= matches.group('href')
				articleNum = matches.group('articleNum')
				hrefArgs=href[href.find("?")+1:].split("&")
				hrefArgsMap={}
				for hrefArg in hrefArgs:
					tmpL=hrefArg.split("=")
					hrefArgsMap[tmpL[0]]=tmpL[1]				
				if self.checkProvisionExist(hrefArgsMap['origin_id'],hrefArgsMap['provider_id'],hrefArgsMap['isEnglish'],hrefArgsMap['content_type']):# check provision exist in target article
					hreflinkTag='<a href="%s" class="link_2" re="T" cate="en_href" >' % (href+"#i"+articleNum,) 
					#get keyword id
					keyword=self.keywordDao.findByContent(matches.group('keyword'))
					keywordId=''
					if keyword:
						keywordId=keyword.id	
					#posTuple=(startPos,endPos,matches.group('astr'),hreflinkTag)	
					posTuple=(startPos,endPos,keywordId,hreflinkTag)	
					posTupleList.append(posTuple)
				self.search(content,endPos,posTupleList)
		posTupleList.sort(lambda posTuple1,posTuple2:-cmp(posTuple1[0],posTuple2[0]))
		return posTupleList 

	def pattern(self,article,posTupleList=[]):
		for posTuple in posTupleList:	
			startPos=posTuple[0]
			endPos=posTuple[1]
			hreflinkTag=posTuple[3]
			article.content=article.content[:startPos]+hreflinkTag+article.content[startPos:endPos]+"</a>"+article.content[endPos:]
			#TODO add cross ref link
		return article

	def process(self,article):
		"""
		override method process(self,article) in parent class
		@param article
		"""	
		if article.contentType == Article.CONTENT_TYPE_LAW:
			article.content=self.addProvisionPosTag(content)
		posTupleList=self.search(article.content)
		article=self.pattern(article,posTupleList)	
		return article

if __name__=="__main__":
	phprocess=ProvisionHyperlinkProcess()
