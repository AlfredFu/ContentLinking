#coding=utf-8

class Keyword(object):
	KEYWORD_TYPE_FULL='F'#标题对应标题全称
	KEYWORD_TYPE_ABBR='A'#标题简称
	KEYWORD_TYPE_MANUAL='M'#手动添加

	def __init__(self,content='',status='',type='',fullTitleKeywordId=''):
		self.content=content
		self.status=status
		self.type=type
		self.fullTitleKeywordId=fullTitleKeywordId
