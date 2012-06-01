from com.entity.Article import * 

class Case(Article):
	def __init__(self):
		Article.__init__(self)
		self.contentType='C'
