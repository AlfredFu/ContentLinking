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
		self.provisionPatternStr=r'(?P<astr>article\s+(?P<articleNum>[\d+\.]+?))\s+of\s+the [\s"]*?(<a href="(?P<href>[^\"^>]*?)" class="link_2" re="T" cate="en_href"\s*>).+?</a>'
		self.provisionPattern=re.compile(self.provisionPatternStr,re.I)
	
	def search(self,content,start=0,posTupleList=[]):
		tmpContent=content[start:]
		if tmpContent:
			matches=self.provisionPattern.search(tmpContent)	
			if matches:
				startPos=start+matches.start(1)
				endPos=start+matches.end(1)
				href= matches.group('href')
				articleNum = matches.group('articleNum')
				hreflinkTag="<a href=\"%s\" class=\"link_2\" re=\"T\" cate=\"en_href\" >" % (href+"#i"+articleNum,) 
				posTuple=(startPos,endPos,matches.group('astr'),hreflinkTag)	
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

if __name__=="__main__":
	phprocess=ProvisionHyperlinkProcess()
	content="""
	The indictment says that Zhang hired another person to forge a resident identity card, and she was found to use this card to apply for overdraft in the bank. Zhang"s act had violated Paragraph 3, Article 280 of the <a href="/law/content.php?content_type=T&origin_id=470853&provider_id=1&isEnglish=Y" class="link_2" re="T" cate="en_href" >Criminal Law of the People"s Republic of China</a> (hereinafter referred to as the <a href="/law/content.php?content_type=T&origin_id=470853&provider_id=1&isEnglish=Y" class="link_2" re="T" cate="en_href" >Criminal Law</a>), and constituted the crime of forging a resident identity card. Jing"an Procuratorate requested Jing"an Court to render a judgment in accordance with the law.
	"""	
	print phprocess.search(content)
