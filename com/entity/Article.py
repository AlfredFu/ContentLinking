#coding=utf-8
class Article(object):
	CONTENT_TYPE_LAW='T'#法规
	CONTENT_TYPE_CASE='C'#案例
	CONTENT_TYPE_NEWS='N'#专题数据
	CONTENT_TYPE_OTHERS='O'#其他
	ACTION_TYPE_NEW='N'
	ACTION_TYPE_UPDATE='U'
	ACTION_TYPE_DEL='D'
	STATUS_AWAIT=1
	STATUS_PROCESSING=3
	STATUS_FINISHED=11
	
	
    	def __init__(self):
        	#self.originId=originId
        	#self.provoiderId=providerId
        	#self.isEnglish=isEnglish
        	#self.contentType=contentType 内容类型
		#self.proDate=proDate 发文日期
		pass
