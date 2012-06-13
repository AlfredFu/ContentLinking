from com.process.KeywordHyperlinkProcess import *

if __name__=='__main__':
	keywordProcess=KeywordHyperlinkProcess()
	#keywordProcess.process()
	i=1
	for queueItem in keywordProcess.queueDao.getAll():
		if i>10:break
		i+=1
		keywordProcess.log.info("keyword process article type:%s id:%s" % (queueItem.contentType,queueItem.targetId))
		keywordProcess.updateOprLoadStatus(queueItem)
		article=keywordProcess.getArticle(queueItem)	
		for keyword in keywordProcess.keywordDao.getAll():
			posTupleList=keywordProcess.findKeywordPosInArticle(keyword,article)
		
		#print posTupleList	
		article=keywordProcess.patternContent(posTupleList,article)
		keywordProcess.updateArticle(article)
		#print article.content


