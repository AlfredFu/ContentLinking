#coding=utf-8
from com.process import *
import re

class AbbreviationHyperlinkProcess(HyperlinkProcess):
	"""
	文章内部简称Hyperlink处理
	"""	
	def __init__(self):
		super(AbbreviationHyperlinkProcess,self).__init__()
		self.abbrTagPatternStr=r'\(hereinafter referred to as the [\'\"]?(?P<abbr>[\w\s]+)[\'\"]?\)'#匹配出现以下简称****的字符串
		self.abbrHyperlinkPatternStr=r'(<a[^<]+?>)([^<]+?)</a>[\'\"]*\s*$'#匹配紧挨着的加上超链接的法规
		self.abbrTagPattern=re.compile(self.abbrTagPatternStr,re.I)
		self.abbrHyperlinkPattern=re.compile(self.abbrHyperlinkPatternStr)

	def findAbbrTagPatternStr(self,content,start=0,abbrPosTupleList=[]):
		"""
		在content中查找self.abbrTagPatternStr
		返回位置信息列表
		列表中元素描述(开始位置startPos,结束位置endPos,简称字符串abbr,全称的超链接开始标签)
		"""
		#print self.abbrTagPattern.findall(content)
		tmpContent=content[start:]
		if tmpContent:
			matches=self.abbrTagPattern.search(tmpContent)
			if matches:
				abbrStr=matches.group(1)
				if abbrStr.strip().find(' ')!=-1:#对于简称为单个单词的简称不做处理
					hyperlinkTag=self.getAbbrHyperlinkTag(content,start=start,end=matches.start()+start)#获取简称前面法规的超链接开始标签
					if hyperlinkTag:
						abbrPosTuple=(matches.start(1)+start,matches.end(1)+start,matches.group(1).strip(),hyperlinkTag)
						abbrPosTupleList.append(abbrPosTuple)
				start=matches.end(1)+start
				self.findAbbrTagPatternStr(content,start,abbrPosTupleList)
		abbrPosTupleList.reverse()
		return abbrPosTupleList

	def checkAbbrInKeywordList(self,abbr):
		"""
		判断简称是否在关键词列表中，如果在返回True,否则返回False
		"""
		return False
	
	def getAbbrHyperlinkTag(self,content,start=0,end=-1):
		"""
		获取简称对应的hyperLink标签
		例如:<a href='/law/content.php?id=32300' class='link_3'>
		"""
		matches=self.abbrHyperlinkPattern.search(content,start,end)
		if matches:
			#print matches.group(1)
			#print matches.group(2)
			return matches.group(1)
	
	def patternContent(self,content,abbrPosTuple,start=0,end=-1):
		"""
		为文章中的简称加上相应的超链接
		"""
		if start<abbrPosTuple[1]:
			start=abbrPosTuple[1]
		#print abbrPosTuple[2]
		abbrPos=content.rfind(abbrPosTuple[2],start,end)
		if abbrPos!=-1:
			content=content[:abbrPos]+abbrPosTuple[3]+abbrPosTuple[2]+"</a>"+content[abbrPos+len(abbrPosTuple[2]):]
			content=self.patternContent(content,abbrPosTuple,start,abbrPos)
		return content
						



def testFindAbbrTagPatternStr():
	content="use this card to apply for overdraft in the bank. Zhang's act had violated Paragraph 3, <a href='#' class='link_3'>Article 280</a> (HereinAfter referred to as the Article 280) of <a href='#'>what,tell me why</a> the <a href='/law/content.php?content_type=T&origin_id=470853&provider_id=1&isEnglish=Y' class='link_3' >Criminal Law of the People Republic of China</a> (hereinafter referred to as the ' CriminalL aw ')"
	abbHypePro=AbbreviationHyperlinkProcess()
	matches=abbHypePro.findAbbrTagPatternStr(content)
	print matches 
	for match in matches:
		content=content[:match[0]]+content[match[1]:]
	#content=content[:matches[0][0]]+content[matches[0][1]:]
	#print content
	
def testPatternContent():
	abbHypePro=AbbreviationHyperlinkProcess()
	content="use this card to apply for overdraft in the bank. Zhang's act had violated Paragraph 3, <a href='#' class='link_3'>Article 280</a> (HereinAfter referred to as the Article 280) of <a href='#'>what,tell me why</a> the <a href='/law/content.php?content_type=T&origin_id=470853&provider_id=1&isEnglish=Y' class='link_3' >Criminal Law of the People Republic of China</a>  Article 280(hereinafter referred to as the ' CriminalL aw ')"
	matches=abbHypePro.findAbbrTagPatternStr(content)
	print matches
	print content
	for match in matches:
		content=abbHypePro.patternContent(content,match)	
	print content

if __name__=="__main__":
	#testFindAbbrTagPatternStr()		
	testPatternContent()

				
