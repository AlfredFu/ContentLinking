# coding=utf-8
from com.dao.LawDAO import *
from com.dao.CaseDAO import *
from com.dao.KeywordDAO import *
from com.dao.HyperlinkQueueDAO import *
import re

class HyperlinkProcess(object):
	def __init__(self):
		pass
	def eraseHyperlink(content):
		"""
		清除hyperlink所加的超链接
		hyperlink sample:<a href='' class='link_2' re='T' cate='en_href' >Criminal Law</a>
		"""	
		content=re.sub(r'<a\s+href=\'[/\w\d\-\.]*?\'\s+class=\'link_2\'\s+re=\'T\'\s+cate=\'en_href\'\s*>(.*?)</a>',r'\1',content)
		return content
	
	def checkHyperlinkedKeyword(content,startPos,endPos):
		"""
		判断关键词是否被加上了超链接,是返回True,否则返回False
		@param content 
		@param startPos关键词在文章中的出现位置
		@param endPos 关键词结尾位置
		"""
		if content:
			startMatch=re.search(r'<a.+?>\s*$',content[:startPos])
			endMatch=re.search(r'^</a\s*>',content[endPos:])
			if startMatch and endMatch:
				return True
		return False

	def selectTargetArticle(article,articleCandidate):
		"""
		对于多个版本的文章(法规)，需要根据发文日期和生效日期的信息选择一个
		param article hyperlink文章，
		param lawCandidate多版本文章(法规)列表
		return 返回文章(文章)对象
		"""
		latestDate=''
		latestArticle=None
		for targetArticle in articleCandidate:
			if article.contentType=='T':#法规以发文日期作为比较日期
				compDate=targetArticle.prodate
			else:
				compDate=max([targetArticle.proDate,targetArticle.effectDate])#其他内容类型以发文日期和生效日期最近的一个作为比较日期
					
			if article.proDate<compDate:continue#发文日期在法规生效日期或法文日期之后，法规不能被引用
			elif latestDate <compDate:
				latestDate=compDate
				latestArticle=targetArticle
		return latestArticle


	def deleteCrossRefLinkById(id):
		"根据文章id删除hyperlink记录"
		crossRefLinkDao=CrossRefLinkDAO()
		crossRefLinkDao.deleteBySrcId(id)
		crossRefLinkDao.deleteByDesId(id)
