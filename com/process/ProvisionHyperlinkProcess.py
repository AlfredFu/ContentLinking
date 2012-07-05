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
		self.mulProviPatn=re.compile(r'',re.I)
		#content type 
        	self.contentTypeMap={'T':'law',\
					'C':'case',\
					'LM':'newlaw',\
					'FL':'foreiginlaw',\
					'PNL':'profnewsletter+journal',\
					'HN':'hotnews',\
					'PC':'pgl_content',\
					'LB':'expert+ex_questions',\
					'LOTP':'tp_overview',\
					'LOFDI':'investment_overview',\
					'LOEP':'ep_overview',\
					'LOEE':'energy_overview',\
					'LOCP':'cp_overview',\
					'LOCS':'cs_overview',\
					'LOIP':'ip_overview',\
					'EL':'ep_elearning',\
					'SUMMARY':'summary',\
					'PEA':'expert+ex_questions'}
		#content type name display in user agent
        	self.contentTypeNameMap={'T':'Legislation',\
					'C':'Case',\
					'LM':'Legal news',\
					'FL':'Foreign law',\
					'PNL':'Newsletters',\
					'HN':'Articles',\
					'PC':'Practical materials',\
					'LB':'Q & A',\
					'LOTP':'Tax overview',\
					'LOFDI':'Investment overview',\
					'LOEP':'Employment overview',\
					'LOEE':'Energy overview',\
					'LOCP':'Corporate overview',\
					'LOCS':'Financing overview',\
					'LOIP':'IP overview',\
					'EL':'Elearning',\
					'SUMMARY':'Overview summary',\
					'PEA':'Q & A'}
        	self.reArticleStart='<br/><font color="red">(Relative article:</font>'
        	self.reArticleEnd='<font color="red">)</font>'

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
			for row in self.crossRefLinkDao.collectRelativeStastics(article.originId,article.providerId,article.isEnglish,article.contentType):
				provisionNum=row[0]#法条序号 
				if provisionNum not in relativeArticleLinkTagMap.keys():
					relativeArticleLinkTagMap[provisionNum]=''
				contentType=row[1]
				if contentType:
					relativeArticleLinkTagMap[provisionNum]+=' <a href="#" onclick="linkage(this,\'%s\',%s,2);return false;" style="text-decoration:underline;color:#00f;">%s</a>' % (self.contentTypeMap[contentType],provisionNum,(self.contentTypeNameMap[contentType]+" %s") % row[2]) 
				
			for key in relativeArticleLinkTagMap.keys():
				provisionEndPos=article.content.find('<a name="end_i%s" re="T"></a>' % key)#TODO think about multiple same provision end tag in one article 
				if provisionEndPos!=-1:
					article.content=article.content[:provisionEndPos]+self.reArticleStart+relativeArticleLinkTagMap[key]+self.reArticleEnd+article.content[provisionEndPos:]
		self.updateArticle(article)

	def removeProvisionRelativeArticleLink(self,content):
		"""
		Remove relative article link for provision
		"""
		content=content.replace(self.reArticleStart,'')	
		content=content.replace(self.reArticleEnd,'')	
		content=re.sub(r' <a href="#" onclick="linkage\(this,\'[\w\+]+?\',\d+,2\);return false;"[^>]*?>[^<]*?</a>','',content)
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
			matches=re.search(r'<a href="(?P<hreflink>[^"^#]*?)#i(?P<proNum>[\d\.]*)" class="link_2" re="T" cate="en_href" >',hreflinkTag)
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
					#print "provisionNum:",provisionNum
					self.addCrossRefLink(article,targetArticle,posTuple[2],provisionNum)
				except Exception,e:
					self.log.error(e)
		return article

	def process(self,article):
		"""
		Override method process(self,article) in parent class
		@param article
		"""	
		posTupleList=self.search(article.content)
		article=self.pattern(article,posTupleList)	
		#print posTupleList
		del posTupleList[:]#清空list,否则会出现记录位置被重复使用的错误
		return article

if __name__=="__main__":
	phprocess=ProvisionHyperlinkProcess()
