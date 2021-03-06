#coding=utf-8
from com.process import *
from com.entity.Article import *
import re

class AbbreviationHyperlinkProcess(HyperlinkProcess):
	"""
	文章内部简称Hyperlink处理
	"""	
	def __init__(self):
		super(AbbreviationHyperlinkProcess,self).__init__()
		self.abbrTagPatternStr=r'\(here(in)?after referred to as (the )?[\'\"]?(?P<abbrStr>[\w\s]+)[\'\"]?\)'#匹配出现以下简称****的字符串
		self.abbrHyperlinkPatternStr=r'(<a[^<]+?>)([^<]+?)</a>[\'\"]*\s*$'#匹配紧挨着的加上超链接的法规
		self.abbrTagPattern=re.compile(self.abbrTagPatternStr,re.I)
		self.abbrHyperlinkPattern=re.compile(self.abbrHyperlinkPatternStr)

	def search(self,content,start=0,posTupleList=[]):
		"""
		在content中查找self.abbrTagPatternStr
		返回位置信息列表
		列表中元素描述(开始位置startPos,结束位置endPos,简称字符串abbr,全称的超链接开始标签)
		"""
		tmpContent=content[start:]
		if tmpContent:
			matches=self.abbrTagPattern.search(tmpContent)
			if matches:
				abbrStr=matches.group('abbrStr')
				if abbrStr.strip().find(' ')!=-1 and not self.checkAbbrInKeywordList(abbrStr):#对于简称为单个单词的简称不做处理,简称在关键词列表中的也不处理
					hyperlinkTag=self.getAbbrHyperlinkTag(content,start=start,end=matches.start()+start)#获取简称前面法规的超链接开始标签
					if hyperlinkTag:
						abbrPosTuple=(matches.start(1)+start,matches.end(1)+start,abbrStr,hyperlinkTag)
						posTupleList.append(abbrPosTuple)
				start=matches.end(0)+start
				posTupleList=self.search(content,start,posTupleList)
		posTupleList.sort(lambda posTuple1,posTuple2: - cmp(posTuple1[0],posTuple2[0]))#根据出现的起始位置排序
		return posTupleList

	def checkAbbrInKeywordList(self,abbr):
		"""
		判断简称是否在关键词列表中，如果在返回True,否则返回False
		"""
		for keyword in self.keywordDao.getAll():
			if keyword.content == abbr:
				return True	
		return False
	
	def getAbbrHyperlinkTag(self,content,start=0,end=None):
		"""
		获取简称对应的hyperLink标签
		例如:<a href="/law/content.php?id=32300" class="link_2" re="T" cate="en_href" target="_blank" >
		"""
		if end:
			matches=self.abbrHyperlinkPattern.search(content,start,end)
		else:
			matches=self.abbrHyperlinkPattern.search(content,start)
		if matches:
			return matches.group(1)
	
	def patternContent(self,content,abbrPosTuple,start=0,end=None):
		"""
		为文章中的简称加上相应的超链接
		@param content 文章内容
		@param abbrPosTuple 文章中某简称第一次出现的位置
		@param start 开始匹配简称的位置，用于控制递归
		@param end 用于控制递归
		"""
		#TODO 简称出现在文章最后，不能被加上超链接
		if start<abbrPosTuple[1]:
			start=abbrPosTuple[1]
		if end:
			abbrPos=content.rfind(abbrPosTuple[2],start,end)
		else:
			abbrPos=content.rfind(abbrPosTuple[2],start)
		
		if abbrPos!=-1:
			if  self.checkTextShouldBeCited(content,abbrPos,abbrPos+len(abbrPosTuple[2])):#if text should be cited
				content=content[:abbrPos]+abbrPosTuple[3]+abbrPosTuple[2]+"</a>"+content[abbrPos+len(abbrPosTuple[2]):]
			content=self.patternContent(content,abbrPosTuple,start,abbrPos)
		return content

	def pattern(self,article,posTupleList=[]):
		for posTuple in posTupleList:
			article.content=self.patternContent(article.content,posTuple)	
		return article


if __name__=="__main__":
	testPatternContent()
