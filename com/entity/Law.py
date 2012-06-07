#coding=utf-8
from com.entity.Article import * 

class Law(Article):
	"法规类"
	def __init__(self):
		Article.__init__(self)
		self.content_type='T'


if __name__=='__main__':
	law=Law()
