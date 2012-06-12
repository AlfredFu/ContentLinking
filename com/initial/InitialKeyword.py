#coding=utf-8
"""
初始化英文关键词
lnc.keyword_en表
"""
from com.dao.KeywordDAO import *

def initial():
	keywordDao=KeywordDAO()
	keywordDao.initialKeyword()
