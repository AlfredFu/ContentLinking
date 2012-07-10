#coding=utf-8
from com.dao.ContentDAO import *
contentDao=ContentDAO()

def cleanBackup():
	contentDao.deleteAll()

def backupArticle(article):
	if article.id and article.contentType and article.content:
		contentDao.add(article.content,article.id,article.contentType)

def rollbackArticle(article):
	if article.id and article.contentType:
		content=contentDao.getByTarget(article.id,article.contentType)
