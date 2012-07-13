#!/usr/bin/env python
from com.process.KeywordHyperlinkProcess import *
from com.process.VersionHyperlinkProcess import *
from com.process.ProvisionHyperlinkProcess import *
from com.process.AbbreviationHyperlinkProcess import *
from com.process.filter import *
from com.util.lexismail import *
from com.util.lexismsg import *


if __name__=='__main__':
	khp=KeywordHyperlinkProcess.KeywordHyperlinkProcess()
	vhp=VersionHyperlinkProcess.VersionHyperlinkProcess()
	phprocess=ProvisionHyperlinkProcess.ProvisionHyperlinkProcess()
	ahp=AbbreviationHyperlinkProcess()

	
	articleList=[('T','230972',1,'Y')]
	for queueItem in khp.queueDao.getAll():
		if (queueItem.contentType,queueItem.originId,queueItem.providerId,queueItem.isEnglish) in articleList:
			#khp.keywordDao.deleteByTarget(article.id,article.contentType)
			#khp.articleDao.deleteByTarget(article.id,article.contentType)
			print "process"
			khp.begin(queueItem)
			article=khp.getArticle(queueItem)
			khp.eraseHyperlink(article)
			khp.removeProvisionPosTag(article)
			if article and article.content:
				khp.log.info("Hyperlink processing article type:%s id:%s" % (queueItem.contentType,queueItem.targetId))
				article=khp.process(article)
				article=vhp.process(article)
				article=ahp.process(article)
				article=phprocess.process(article)
				khp.updateArticle(article)
			else:
				khp.log.warning("Article type:%s id:%s was not found" %(queueItem.contentType,queueItem.targetId))
			khp.end(queueItem)
	
	for queueItem in khp.queueDao.getByContentTypeStatus(Article.CONTENT_TYPE_LAW,Article.STATUS_WAIT_UPLOAD):
		if (queueItem.contentType,queueItem.originId,queueItem.providerId,queueItem.isEnglish) in articleList:
			article=phprocess.getArticle(queueItem)
			if article and article.content:
				article.content=phprocess.removeProvisionRelativeArticleLink(article.content)
				phprocess.addProvisionRelativeArticleLink(article)
			else:
				khp.log.warning("Article type:%s id:%s was not found" %(queueItem.contentType,queueItem.targetId))

