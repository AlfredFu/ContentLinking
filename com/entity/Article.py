#coding=utf-8
class Article(object):
	"""
	文章
	"""
	CONTENT_TYPE_LAW='T'#法规
	CONTENT_TYPE_CASE='C'#案例
	CONTENT_TYPE_NEWSLETTER='PNL'#专业期刊
	CONTENT_TYPE_LNCQA='LB'#LNC Q & A
	CONTENT_TYPE_MODULEQA='PEA'#专题 Q & A
	CONTENT_TYPE_NEWLAW='LM'#legal news
	CONTENT_TYPE_HOTNEWS='HN'#评论文章
	CONTENT_TYPE_TPOVERVIEW='LOTP'#税法实务概览
	CONTENT_TYPE_FDIOVERVIEW='LOFDI'#外商投资实务概览
	CONTENT_TYPE_EPOVERVIEW='LOEP'#劳动法实务概览
	CONTENT_TYPE_EEOVERVIEW='LOEE'#能源与环境实务概览
	CONTENT_TYPE_CPOVERVIEW='LOCP'#公司法实务概览
	CONTENT_TYPE_CSOVERVIEW='LOCS'#公司融资实务概览
	CONTENT_TYPE_IPOVERVIEW='LOIP'#知识产权实务概览
	CONTENT_TYPE_OVERVIEW_SUMMARY='SUMMARY'
	CONTENT_TYPE_ELEARNING='EL'
	CONTENT_TYPE_PRACTICAL='PC'#实用资料
	CONTENT_TYPE_FOREIGNLAW='FL'
	CONTENT_TYPE_NEWS='N'#专题数据
	CONTENT_TYPE_OTHERS='O'#其他

	ACTION_TYPE_NEW='N'
	ACTION_TYPE_UPDATE='U'
	ACTION_TYPE_DELETE='D'

	STATUS_AWAIT=1#await to be processed
	STATUS_PROCESSING=3#article being processed
	STATUS_WAIT_UPLOAD=9#ready to be uploaded to prd
	STATUS_FINISHED=11#process finished
	
	
    	def __init__(self):
		#self.id=id
        	#self.originId=originId
        	#self.provoiderId=providerId
        	#self.isEnglish=isEnglish
        	#self.contentType=contentType 内容类型
		#self.proDate=proDate 发文日期
		pass

	def __eq__(self,other):
		if other and self.originId==other.originId and self.providerId == other.providerId and self.isEnglish==other.isEnglish and self.contentType==other.contentType:
			return 1
		return 0	
