# coding=utf-8
from com.dao.LawDAO import *
from com.dao.CaseDAO import *
from com.dao.KeywordDAO import *
from com.dao.HyperlinkQueueDAO import *
import re

class HyperlinkProcess(object):
	def __init__(self):
		self.crossRefLinkDao=CrossRefLinkDAO()
		self.lawDao=LawDAO()
		self.caseDao=CaseDAO()
		self.keywordDao=KeywordDAO()
		self.queueDao=HyperlinkQueueDAO()
		pass
	def eraseHyperlink(self,content):
		"""
		清除hyperlink所加的超链接
		hyperlink sample:<a href='' class='link_2' re='T' cate='en_href' >Criminal Law</a>
		"""	
		content=re.sub(r'<a\s+href=\'[/\w\d\-\.]*?\'\s+class=\'link_2\'\s+re=\'T\'\s+cate=\'en_href\'\s*>(.*?)</a>',r'\1',content)
		return content
	
	def checkHyperlinkedKeyword(self,content,startPos,endPos):
		"""
		判断关键词是否被加上了超链接,是返回True,否则返回False
		@param content 
		@param startPos关键词在文章中的出现位置
		@param endPos 关键词结尾位置
		"""
		if content:
			startMatch=re.search(r'<a.+?>\s*$',content[:startPos])#在关键字出现位置前找锚标记a开始标签
			endMatch=re.search(r'^</a\s*>',content[endPos:])#在关键字出现位置后找锚标记结束符
			if startMatch and endMatch:
				return True
		return False

	def selectTargetArticle(self,article,articleCandidate):
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

	def updateArticle(self,article):
		"""
		做完hyperlink后更新相关文章的时间
		"""
		if article.contentType=='T':
			self.lawDao.update(article)
		elif article.contentType=='C':
			self.caseDao.update(article)
		else:
			self.exNewsDao.update(article)

	def deleteCrossRefLinkByArticleId(self,id):
		"根据文章id删除hyperlink记录"
		self.crossRefLinkDao.deleteBySrcId(id)
		self.crossRefLinkDao.deleteByDesId(id)

	def getRelatedArticleId(self,id):
		pass
		

	def updateRelatedArticleActionType(self,article):
		"""
		将相关文章的action_type属性改为U
		"""
		for item in crossRefLinkDao.getRelatedArticleId(article.id):
			
	def updateOprLoadStatus(self,queueItem):
		"""
		更新队列中文章的状态
		"""
		if queueItem.contentType =='T':
			if article.actionType == 'D':
				#TODO找出相关文章，更新相关文章的在hyperlink队列中的状态为U
				self.deleteCrossRefLinkByArticleId(queueItem.targetId)#删除cross_ref_link表中的记录
				#TODO hyperlink处理
				pass
			elif article.actionType=='N':
				#TODO更新队列中状态为空的数据状态为U
				#TODO hyperlink处理
				pass
			elif article.actionType=='U':
				#TODO找出相关文章，更新相关文章的在hyperlink队列中的状态为U
				self.deleteCrossRefLinkByArticleId(queueItem.targetId)		
				#hyperlink处理
				pass
		else:
			if queueItem.actionType == 'D':
				self.deleteCrossRefLinkByArticleId(queueItem.targetId)		
			elif queueItem.actionType =='N':
				#TODO hyperlink处理
				pass
			elif queueItem.actionType =='U':
				self.deleteCrossRefLinkByArticleId(queueItem.targetId)		
							
