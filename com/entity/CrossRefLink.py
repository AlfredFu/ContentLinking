class CrossRefLink(object):
	def __init__(self):
		super(CrossRefLink,self).__init__()
		pass
	
	def toTuple(self):
		"""
		将对象转为元组
		"""
		return (self.srcArticleId,self.keywordId,self.desArticleId,self.desItemId,self.attachementId,self.srcContentType,self.srcOriginId,self.srcProviderId,self.srcIsEnglish,self.desContentType,self.desOriginId,self.desProviderId,self.desIsEnglish)
