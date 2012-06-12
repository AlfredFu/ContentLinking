#coding=utf-8
from com.dao.HyperlinkQueueDAO import *
from com.dao.CaseDAO import * 
from com.dao.LawDAO import *
from com.dao.ExNewsDAO import *
from com.dao.KeywordDAO import *
from com.entity.Keyword import *
from com.dao.ArticleDAO import *

"""
hyperlink文章记录表
lnc.article_en表
"""
caseDao=CaseDAO()
lawDao=LawDAO()
exNewsDao=ExNewsDAO()
keywordDao=KeywordDAO()
articleDao=ArticleDAO()

articleList=[]

for article in caseDao.getAll():
	articleList.append((article.contentType,article.originId,article.providerId,article.isEnglish,article.id,'N','1',''))

for article in exNewsDao.getAll():
	articleList.append((article.contentType,article.originId,article.providerId,article.isEnglish,article.id,'N','1',''))

p=re.compile(r'\(revised in [0-9]{4}\)$',re.I)
ss=re.compile(r'of the People\'s Republic of China',re.I)
for article in lawDao.getAll():
	keyword=Keyword()
	keyword.content=p.sub('',article.title)
	keyword.type=Keyword.KEYWORD_TYPE_FULL
	keywordId=keywordDao.add(keyword)
	articleList.append((article.contentType,article.originId,article.providerId,article.isEnglish,article.id,'N','1',keywordId))
	if ss.search(keyword.content):
		abbrKeyword=Keyword()
		abbrKeyword.content=ss.sub('',keyword.content)	 
		abbrKeyword.type=Keyword.KEYWORD_TYPE_ABBR
		keywordDao.add(abbrKeyword)

articleDao.addMany(articleList)
