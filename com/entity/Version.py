class Version:
	def __init__(self):
		self.srcOriginId=''
		self.srcProviderId=''
		self.srcIsEnglish=''
		self.desOriginId=''
		self.desProviderId=''
		self.desIsEnglish=''
	
	def toTuple(self):
		"""
		对象数据转换为元组
		"""
		return (self.srcOriginId,self.srcProviderId,self.srcIsEnglish,self.desOriginId,self.desProviderId,self.desIsEnglish)
		
