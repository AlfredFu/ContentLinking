from com.process.KeywordHyperlinkProcess import *
from com.process.VersionHyperlinkProcess import *
from com.process.AbbreviationHyperlinkProcess import *


if __name__=='__main__':
	khp=KeywordHyperlinkProcess.KeywordHyperlinkProcess()
	vhp=VersionHyperlinkProcess.VersionHyperlinkProcess()
	ahp=AbbreviationHyperlinkProcess()
	
	for queueItem in khp.queueDao.getAll():
		khp.begin(queueItem)
		article=khp.getArticle(queueItem)
		article=khp.process(article)
		article=vhp.process(article)
		article=ahp.process(article)
		khp.updateArticle(article)
		khp.end(queueItem)
