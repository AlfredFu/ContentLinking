#coding=utf-8

class Keyword(object):
	"""
	English keyword store in table 'keyword_en' of database 'lnc'
	All the keyword is comprised of lower case
	"""
	KEYWORD_TYPE_FULL='F'#标题对应标题全称
	KEYWORD_TYPE_ABBR='A'#标题简称
	KEYWORD_TYPE_MANUAL='M'#手动添加

	def __init__(self):
		self.content=''
		self.status=''
		self.type=Keyword.KEYWORD_TYPE_FULL
		self.fullTitleKeywordId=''
