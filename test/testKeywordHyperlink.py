from com.process.KeywordHyperlinkProcess import *

"""
	def process(self,article=None):
		for queueItem in self.queueDao.getAll():
			self.updateOprLoadStatus(queueItem)
			article=self.getArticle(queueItem)	
			for keyword in self.keywordDao.getAll():
				posTupleList=self.search(keyword,article)
				
			article=self.pattern(posTupleList,article)
			self.updateArticle(article)
			print article.content

	def process(self,article):
		for keyword in self.keywordDao.getAll():
			posTupleList=self.search(keyword,article)
		article=self.pattern(posTupleList,article)
		#self.updateArticle(article)
		return article
"""
		



if __name__=='__main__':
	keywordProcess=KeywordHyperlinkProcess()
	#keywordProcess.process()
	i=1
	for queueItem in keywordProcess.queueDao.getAll():
		if i>1:break
		i+=1
		article=keywordProcess.getArticle(queueItem)	
		#print article.content
		#print "======================================================================================================="
		#print article.id,article.title	
		keywordProcess.log.info("keyword process article type:%s id:%s" % (queueItem.contentType,queueItem.targetId))
		print "keyword process article type:%s id:%s" % (queueItem.contentType,queueItem.targetId)
		print "======================================================================================================="
		#keywordProcess.updateOprLoadStatus(queueItem)
		article.content=keywordProcess.eraseHyperlink(article.content)
		"""
		for keyword in keywordProcess.keywordDao.getAll():
			posTupleList=keywordProcess.findKeywordPosInArticle(keyword,article)
		article=keywordProcess.patternContent(posTupleList,article)
		"""
		#print keywordProcess.search(article.content)
		article=keywordProcess.process(article)
		#print article.content
		#print article.content
		keywordProcess.updateArticle(article)
