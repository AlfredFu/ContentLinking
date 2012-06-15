from com.process.KeywordHyperlinkProcess import *

if __name__=='__main__':
	keywordProcess=KeywordHyperlinkProcess()
	#keywordProcess.process()
	i=0
	for queueItem in keywordProcess.queueDao.getAll():
		i+=1
		if i<101:continue
		if i>200:break
		#keywordProcess.updateArticle(article)
		#print article.content
		#keywordProcess.log.info("keyword process article type:%s id:%s" % (queueItem.contentType,queueItem.targetId))
		#keywordProcess.updateOprLoadStatus(queueItem)
		article=keywordProcess.getArticle(queueItem)	
		#article.content=keywordProcess.eraseHyperlink(article.content)
		for keyword in keywordProcess.keywordDao.getAll():
			posTupleList=keywordProcess.findKeywordPosInArticle(keyword,article)
		#posTupleList=[(12450, 12462, 155575636L, 'Criminal Law', 155570023L), (9918, 9930, 155575636L, 'Criminal Law', 155570023L), (9586, 9598, 155575636L, 'Criminal Law', 155570023L), (9074, 9086, 155575636L, 'Criminal Law', 155570023L), (7908, 7920, 155575636L, 'Criminal Law', 155570023L), (7164, 7176, 155575636L, 'Criminal Law', 155570023L), (6956, 6968, 155575636L, 'Criminal Law', 155570023L), (4737, 4749, 155575636L, 'Criminal Law', 155570023L), (1123, 1135, 155575636L, 'Criminal Law', 155570023L), (938, 984, 155570023L, 'Criminal Law of the People\'s Republic of China', None)]	
		#print posTupleList	
		#article=keywordProcess.patternContent(posTupleList,article)
		#print article.content
		#keywordProcess.updateArticle(article)
		#print article.content
