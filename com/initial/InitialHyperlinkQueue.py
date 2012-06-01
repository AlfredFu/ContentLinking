from com.dao.HyperlinkQueueDAO import *
from com.dao.CaseDAO import * 

caseDao=CaseDAO()
hyperlinkQueueDao=HyperlinkQueueDAO.HyperlinkQueueDAO()
caseQueueItem=[]
for case in caseDao.getCase():
	caseQueueItem.append((case.contentType,case.originId,case.providerId,case.isEnglish,case.id,'N',1))
	hyperlinkQueueDao.addMany(caseQueueItem)
