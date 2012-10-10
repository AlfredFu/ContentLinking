# coding=utf-8
from com.process import *
from com.util.urlutil import *
import re

class ProvisionHyperlinkProcess(HyperlinkProcess):
	"""
	process provision hyperlink
	"""
	def __init__(self):
		super(ProvisionHyperlinkProcess,self).__init__()
		self.mulProviPatn=re.compile(r'(?P<p1>articles?\s+(?P<p11>[\d\.]+))\s*(?P<p2>(,\s*[\d\.]+\s*)*)(\s+(and|or)\s+(?P<p3>[\d\.]+))?\s+of\s+(the)?[\s"]*?(<a href="(?P<href>[^\"^>]*?)"[^>]*?cate="en_href"[^>]*?>)(?P<keyword>.+?)</a>',re.I)
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
					'LOMA':'ma_overview',\
					'EL':'ep_elearning',\
					'SUMMARY':'summary',\
					'PEA':'expert+ex_questions'}
        	self.reArticleStart='<br/><font color="red">(Relevant articles:</font><font color="blue">'
        	self.reArticleEnd='</font><font color="red">)</font>'
		self.provisionStartTagFormat='<a name="i%s" re="T"></a>'
		self.provisionEndTagFormat='<a name="end_i%s" re="T"></a>'

		self.linkageTagFormat=' <a href="#" onclick="linkage(this,\'%s\',%s,2);return false;" style="text-decoration:underline;color:#00f;">%s</a>'
		self.linkageTagPattern=re.compile(r' <a href="#" onclick="linkage\(this,\'[\w\+]+?\',\d+,2\);return false;"[^>]*?>[^<]*?</a>',re.I)	

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
			if article.content.count(self.provisionStartTagFormat % provisionNum)==1:
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
				if provisionNum not in relativeArticleLinkTagMap:
					relativeArticleLinkTagMap[provisionNum]=''
				contentType=row[1]
				if contentType:
					relativeArticleLinkTagMap[provisionNum]+=self.linkageTagFormat % (self.contentTypeMap[contentType],provisionNum,(self.contentTypeNameMap[contentType]+" %s") % row[2]) 
				
			for key in relativeArticleLinkTagMap:
				#TODO think about multiple same provision end tag in one article 
				provisionEndPos=article.content.find(self.provisionEndTagFormat % key)
				if provisionEndPos!=-1:
					article.content=article.content[:provisionEndPos]+self.reArticleStart+relativeArticleLinkTagMap[key]+self.reArticleEnd+article.content[provisionEndPos:]
		self.updateArticle(article)

	def removeProvisionRelativeArticleLink(self,content):
		"""
		Remove relative article link for provision
		"""
		if content:
			content=content.replace(self.reArticleStart,'')	
			content=content.replace(self.reArticleEnd,'')	
			content=self.linkageTagPattern.sub('',content)
		return content
 
	def getOriginByHref(self,href):
		"""
		Get origin id,provider id and isEnglish by hreflink
		return param map of hreflink href
		"""	
		return getUrlParams(href)

	def search(self,content,start=0,posTupleList=[]):
		tmpContent=content[start:]
		if tmpContent:
			matches=self.mulProviPatn.search(tmpContent)	
			if matches:
				provisionNumList=[]
				#匹配连续出现的法条第一条
				if matches.group('p1'):
					startPos=start+matches.start('p1')
					endPos=start+matches.end('p1')
					provisionNum=matches.group('p11')
					provisionNumList.append((startPos,endPos,provisionNum))

				#匹配连续出现的中间法条
				if matches.group('p2'):
					startPos=start+matches.start('p2')
					for tpn in matches.group('p2').split(','):
						if tpn:
							endPos=startPos+len(tpn)
							provisionNum=tpn.strip()	
							provisionNumList.append((startPos,endPos,provisionNum))
						startPos+=(len(tpn)+1)#','长度为一所以要加上

				#匹配连续出现的法条最后一条
				if matches.group('p3'):
					startPos=start+matches.start('p3')
					endPos=start+matches.end('p3')
					provisionNum=matches.group('p3')
					provisionNumList.append((startPos,endPos,provisionNum))

				href= matches.group('href')
				hrefArgsMap=self.getOriginByHref(href)
				try:
					originId=hrefArgsMap['origin_id']
					providerId=hrefArgsMap['provider_id']
					isEnglish=hrefArgsMap['isEnglish']
					contentType=hrefArgsMap['content_type']
				except Exception,e:
					self.log.error("Illegal url format!")
				else:
					for provisionNumTuple in provisionNumList:
						if self.checkProvisionExist(provisionNumTuple[2],originId,providerId,isEnglish,contentType):# check provision exist in target article
							hreflinkTag=self.startLinkTagFormat % (href+"#i"+provisionNumTuple[2]) 
							keyword=self.keywordDao.findByContent(matches.group('keyword'))#get keyword id by keyword str
							keywordId=''
							if keyword:
								keywordId=keyword.id	
							posTuple=(provisionNumTuple[0],provisionNumTuple[1],keywordId,hreflinkTag)	
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
			matches=self.startLinkTagPattern.search(hreflinkTag)
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
		del posTupleList[:]#清空list,否则会出现记录位置被重复使用的错误
		return article

if __name__=="__main__":
	phprocess=ProvisionHyperlinkProcess()
