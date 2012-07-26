#coding=utf-8
from com.transfer.transfer import *
from com.dao.backupdao import *

backupContentDao=ContentDAO()
backupVersionDao=VersionDAO()
backupCrossRefLinkDao=CrossRefLinkDAO()

def cleanBackup():
	backupContentDao.deleteAll()
	backupVersionDao.cleanup()
	backupCrossRefLinkDao.cleanup()

def backupArticle(article):	
	if article.id and article.contentType and article.content:
		backupContentDao.add(article.content,article.id,article.contentType,article.originId,article.providerId,article.isEnglish)

def backupVersions():
	"""
	Backup data in table newlaw_stg.versions
	"""
	backupVersionDao.backup()

def backupCrossRefLinkEn():
	"""
	Backup data in table newlaw_stg.cross_ref_link_en
	"""
	backupCrossRefLinkDao.backup()

def rollbackArticle():
	for article in backupContentDao.getAll():
		if article.id and article.contentType:
			updateArticle(article,isTransfer=False)	
			#文章在队列中的状态回滚
			queueDao.updateStatus(article.id,article.contentType,Article.STATUS_WAIT_UPLOAD)

def rollbackQueueStatus():
	for article in backupContentDao.getAll():
		if article.id and article.contentType:
			queueDao.updateStatus(article.id,article.contentType,Article.STATUS_AWAIT)
	
def rollbackVersions():
	backupVersionDao.rollback()

def rollbackCrossRefLink():
	backupCrossRefLinkDao.rollback()

def backupData():
	cleanBackup()
	backupVersions()
	backupCrossRefLinkEn()	
	
def rollbackData():
	rollbackVersions()
	rollbackCrossRefLink()
	rollbackArticle()
	transferData()#将回滚后的数据传到PRD环境
	rollbackQueueStatus()#文章在队列中的状态回滚到1
	#cleanBackup()
	

if __name__=='__main__':
	rollbackData()
