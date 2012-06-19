from com.process.ProvisionHyperlinkProcess import *

if __name__=='__main__':
	keywordProcess=ProvisionHyperlinkProcess()
	#keywordProcess.process()
	i=1
	for queueItem in keywordProcess.queueDao.getAll():
		if i>1:break
		i+=1
		article=keywordProcess.getArticle(queueItem)	
		print article.content
		#print "======================================================================================================="
		#print article.id,article.title	
		keywordProcess.log.info("keyword process article type:%s id:%s" % (queueItem.contentType,queueItem.targetId))
		print "keyword process article type:%s id:%s" % (queueItem.contentType,queueItem.targetId)
		print "======================================================================================================="
		#keywordProcess.updateOprLoadStatus(queueItem)
		#article.content=keywordProcess.eraseHyperlink(article.content)
		posTupleList=keywordProcess.search(article.content)
		article=keywordProcess.pattern(article,posTupleList)
		#print posTupleList
		print article.content
		#print article.content
		keywordProcess.updateArticle(article)
