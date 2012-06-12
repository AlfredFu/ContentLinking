#coding=utf-8
from com.entity.Article import * 

class ExNews(Article):
	"""
	评论文章，法规解析，案例解析等存放在ex_news表中的数据
	"""

	def __init__(self):
		super(ExNews,self).__init__()
		self.contentType=Article.CONTENT_TYPE_NEWS
