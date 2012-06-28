# coding=utf-8
from com.process import *
import re

class ProvisionHyperlinkProcess(HyperlinkProcess):
	"""
	process provision hyperlink
	"""
	def __init__(self):
		super(ProvisionHyperlinkProcess,self).__init__()
		#self.provisionPatternStr=r"(?P<astr>article\s+(?P<articleNum>\d+\.?\d+))\s+of\s+the\s+(<a href=\"(?P<href>[^\"^>]*?)\" class=\"link_2\" re=\"T\" cate=\"en_href\"\s*>).+?</a>"
		self.provisionPatternStr=r'(?P<astr>article\s+(?P<articleNum>[\d+\.]+?))\s+of\s+the [\s"]*?(<a href="(?P<href>[^\"^>]*?)" class="link_2" re="T" cate="en_href"\s*>)(?P<keyword>.+?)</a>'
		self.provisionPattern=re.compile(self.provisionPatternStr,re.I)
        	self.contentTypeMap={'T':'law','C':'case','LM':'newlaw','FL':'foreiginlaw','PNL':'profnewsletter+journal','HN':'hotnews','PC':'pgl_content','LB':'expert+ex_questions','LOTP':'tp_overview','LOFDI':'','EL':'','PEA':''}
        	self.contentTypeNameMap={'T':'Relative law','C':'Case','LM':'Legal news','FL':'Foreign law','PNL':'Newsletters','HN':'Articles','PC':'Practical materials','LB':'Q & A','LOTP':'TP overview','LOFDI':'','EL':'Elearning','PEA':''}
        	self.langRelativeArticle='<br/><font color="red">Relative article:</font>'

	def addProvisionPosTag(self,content):
		"""
		Mark provision position with following html tag(will not be displayed):
		Mark start position with:<a name="i2" re="T"></a>
		Mark end position with:<a name="end_i1" re="T"></a>
		@param content
		return content after marked with html tag
		"""	
		#provisionStartPattern=re.compile(r'(article ([\d\.]+)(.+\n?.+)+)(\n{1,})',re.I)
		#provisionStartPattern=re.compile(r'^(Article ([\d\.]+)(.+\n?.+)+)(\n{2})',re.MULTILINE)
		#provisionStartPattern=re.compile(r'(\n{2,})(article ([\d\.]+)(.+\n?.+)+)(\n{2,})',re.I)
		provisionStartPattern=re.compile(r'(Article ([\d\.]+).?(.\n?)+?.?)(\n\n|<br />\n?<br />)',re.I)
		content=provisionStartPattern.sub(r'<a name="i\2" re="T"></a>\1<a name="end_i\2" re="T"></a>\4',content)
		#content=provisionStartPattern.sub(r'<a name="i\2" re="T"></a>\1<a name="end_i\2" re="T"></a>\4',content)	
		#content=provisionStartPattern.sub(r'\1<a name="i\3" re="T"></a>\2<a name="end_i\3" re="T"></a>\5',content)	
		return content

	def removeProvisionPosTag(self,content):
		"""
		Remove provision position mark in content
		@param content
		return 
		"""
		return re.sub(r'<a name="(end_)?i[\d\.]+" re="T"></a>','',content)

	def checkProvisionExist(self,provisionNum,originId,providerId,isEnglish='Y',contentType='T'):
		"""
		Check provision is exist in target article which specified by param originId,providerId,isEnglish and contentType
		@param provisionNum provision number
		return if provision exist in target article return True
		else return False
		(If multiple provision with the same number if found ,False will be returned)
		"""
		article=self.getArticleByOrigin(originId,providerId,isEnglish,contentType)
		if article and provisionNum:
			if article.content.count('<a name="i%s" re="T"></a>' % provisionNum)==1:
				return True
		return False 
                     
	def addProvisionRelativeArticleLink(self,article):
		"""
		Add relative article link for provision
		"""
		if article:
			relativeArticleLinkTagMap={} 
			provisionNum=0
			for row in self.crossRefLinkDao.collectRelativeStastics(article.originId,article.providerId,article.isEnglish,article.contentType):
				if provisionNum !=row[0]:
					tmpLinkTag=self.langRelativeArticle#reset variable tmpLinkTag
					provisionNum=row[0]
				contentType=row[1]
				tmpLinkTag+=" <a href='#' onclick='linkage(this,%s,%s,2);return false;' style='text-decoration:underline;color:#00f;'>%s</a>" (self.contentTypeMap[contentType],provisionNum,(self.contentTypeNameMap[contentType]+' %s') % row[2]) 
				relativeArticleLinkTagMap[provisionNum]=tmpLinkTag
			for key in relativeArticleLinkTagMap:
				provisionEndPos=article.content.find('<a name="end_i%s" re="T"></a>' % key)#TODO think about multiple same provision end tag in one article 
				if provisionEndPos:
				    article.content=article.content[:provisionEndPos]+relativeArticleLinkTagMap[key]+article.content[provisionEndPos:]
		self.updateArticle(article)

	def removeProvisionRelativeArticleLink(self,content):
		"""
		Remove relative article link for provision
		"""
		content=content.replace(self.langRelativeArticle,'')	
		content=re.sub(r" <a href='#' onclick='linkage(this,[\w\+]+?,\d+,2);return false;'[^>]*?>[^<]*?</a>",'',content)
		return content
 
	def getOriginByHref(self,href):
		"""
		Get origin id,provider id and isEnglish by hreflink
		return param map of hreflink href
		"""	
		hrefArgs=href[href.find("?")+1:].split("&")
		hrefArgsMap={}
		for hrefArg in hrefArgs:
			tmpL=hrefArg.split("=")
			hrefArgsMap[tmpL[0]]=tmpL[1]				
		return hrefArgsMap
	
	def search(self,content,start=0,posTupleList=[]):
		tmpContent=content[start:]
		if tmpContent:
			matches=self.provisionPattern.search(tmpContent)	
			if matches:
				startPos=start+matches.start(1)
				endPos=start+matches.end(1)
				href= matches.group('href')
				articleNum = matches.group('articleNum')
				hrefArgsMap=self.getOriginByHref(href)
				if self.checkProvisionExist(articleNum,hrefArgsMap['origin_id'],hrefArgsMap['provider_id'],hrefArgsMap['isEnglish'],hrefArgsMap['content_type']):# check provision exist in target article
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
			# add cross ref link
			matches=re.search(r'<a href="(?P<hreflink>[^"^#]*?)#(?P<proNum>[\d\.]*)" class="link_2" re="T" cate="en_href" >',hreflinkTag)
			if matches: 
				hreflink=matches.group('hreflink')#target linked url
				provisionNum=matches.group('proNum')#provision number in article
				hrefArgsMap=self.getOriginByHref(hreflink)
				try:
					originId=hrefArgsMap['origin_id']
					providerId=hrefArgsMap['provider_id']
					isEnglish=hrefArgsMap['isEnglish']
					contentType=hrefArgsMap['content_type']
					targetArticle=self.getArticleByOrigin(originId,providerId,isEnglish,contentType)
					self.addCrossRef(article,targetArticle,posTuple[2],provisionNum)
				except Exception,e:
					self.log.error(e)
					self.log.error("Add cross ref link failed in pattern method of ProvisionHyperlinkProcess.py")
		return article

	def process(self,article):
		"""
		Override method process(self,article) in parent class
		@param article
		"""	
		if article.contentType == Article.CONTENT_TYPE_LAW and article.actionType in [Article.ACTION_TYPE_NEW,Article.ACTION_TYPE_UPDATE]:#if article is law and 
			article.content=self.removeProvisionPosTag(article.content)
			article.content=self.addProvisionPosTag(article.content)
		posTupleList=self.search(article.content)
		article=self.pattern(article,posTupleList)	
		return article

if __name__=="__main__":
	phprocess=ProvisionHyperlinkProcess()
