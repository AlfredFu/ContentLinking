from com.dao.HyperlinkQueueDAO import *
from com.entity.Article import *
import re

def initialArticle(article):
	pass

def initialKeyword(article):
	if article and article.contentType==Article.CONTENT_TYPE_LAW:
		if article.actionType==Article.ACTION_TYPE_NEW:
			keyword=Keyword()
			keyword.content=re.sub(r'\(revised in [0-9]{4}\)$','',article.title)
			if re.search(r'of the People\'s Republic of China',keyword.content):
				abbrKeyword=Keyword()
				abbrKeyword.content=re.sub(r'of the People\'s Republic of China','',keyword.content,flags=re.I)
				abbrKeyword.type=Keyword.KEYWORD_TYPE_ABBR
				abbrKeyword.fullTitleKeywordId=keywordId
				self.keywordDao.add(abbrKeyword)
			article.keywordId=keywordId
			
	pass
def getArticle(queueItem):
	
def initial():
	queueDao=HyperlinkQueueDAO.HyperlinkQueueDAO()	
	for queueItem in queueDao.getAll(): 
		article=
	
