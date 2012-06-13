#coding=utf-8
class CrossRefLink(object):
	def __init__(self):
		super(CrossRefLink,self).__init__()
		self.srcArticleId=''
		self.keywordId=''
		self.desArticleId=''
		self.desItemId=''
		self.desAttachmentId=''
		self.srcContentType=''
		self.srcOriginId=''
		self.srcProviderId=''
		self.srcIsEnglish=''
		self.desContentType=''
		self.desOriginId=''
		self.desProviderId=''
		self.desIsEnglish=''
	
	def toTuple(self):
		"""
		将对象转为元组
		"""
		return (self.srcArticleId,self.keywordId,self.desArticleId,self.desItemId,self.desAttachmentId,self.srcContentType,self.srcOriginId,self.srcProviderId,self.srcIsEnglish,self.desContentType,self.desOriginId,self.desProviderId,self.desIsEnglish)
