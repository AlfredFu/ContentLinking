from com.process.KeywordHyperlinkProcess import *
from com.process.VersionHyperlinkProcess import *
from com.process.ProvisionHyperlinkProcess import *
from com.process.AbbreviationHyperlinkProcess import *
from com.process.filter import *
from com.util.lexismail import *


if __name__=='__main__':
	khp=KeywordHyperlinkProcess.KeywordHyperlinkProcess()
	vhp=VersionHyperlinkProcess.VersionHyperlinkProcess()
	phprocess=ProvisionHyperlinkProcess.ProvisionHyperlinkProcess()
	ahp=AbbreviationHyperlinkProcess()

	#initial phase	 
	khp.initial()	

	#process phase
	for queueItem in khp.queueDao.getAll():
		#debug code
		#begin
		if articleList and (queueItem.contentType,queueItem.originId,queueItem.providerId,queueItem.isEnglish) not in articleList:
			continue
		#print queueItem.targetId,queueItem.contentType
		#end
		khp.begin(queueItem)
		article=khp.getArticle(queueItem)
		if article and article.content:
			khp.log.info("Keyword hyperlink processing article type:%s id:%s" % (queueItem.contentType,queueItem.targetId))
			article=khp.process(article)
			khp.log.info("Version hyperlink  processing article type:%s id:%s" % (queueItem.contentType,queueItem.targetId))
			article=vhp.process(article)
			khp.log.info("Abbreviation hyperlink  processing article type:%s id:%s" % (queueItem.contentType,queueItem.targetId))
			article=ahp.process(article)
			khp.log.info("Provision hyperlink  processing article type:%s id:%s" % (queueItem.contentType,queueItem.targetId))
			article=phprocess.process(article)
			khp.updateArticle(article)
		else:
			khp.log.warning("Article type:%s id:%s was not found" %(queueItem.contentType,queueItem.targetId))
		khp.end(queueItem)
	
	for queueItem in khp.queueDao.getByContentTypeStatus(Article.CONTENT_TYPE_LAW,Article.STATUS_WAIT_UPLOAD):
		article=phprocess.getArticle(queueItem)
		if article and article.content:
			article.content=phprocess.removeProvisionRelativeArticleLink(article.content)
			phprocess.addProvisionRelativeArticleLink(article)
		else:
			khp.log.warning("Article type:%s id:%s was not found" %(queueItem.contentType,queueItem.targetId))

	sendMail('fred.fu@lexisnexis.com')	
