#coding=utf-8
from com.entity.Article import * 

class Law(Article):
	"法规类"
	def __init__(self):
		Article.__init__(self)
		self.contentType=Article.CONTENT_TYPE_LAW


if __name__=='__main__':
	law=Law()
