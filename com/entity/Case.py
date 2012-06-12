#coding=utf-8
from com.entity.Article import * 

class Case(Article):
	"案例类"
	def __init__(self):
		Article.__init__(self)
		self.contentType=Article.CONTENT_TYPE_CASE
