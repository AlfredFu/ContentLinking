#coding=utf-8

class QueueItem:
	"""
	Hyperlink队列中的一个元素,描述一篇文章和文章的hyperlink状态信息
	"""
	STATUS_AWAIT=1
	STATUS_PROCESSING=3
	STATUS_FINISHED=11
	ACTION_TYPE_NEW='N'
	ACTION_TYPE_UPDATE='U'
	ACTION_TYPE_DEL='D'
	
	def __init__(self):
		#opr_id
		#content_type
		#origin_id
		#provider_id
		#is_english
		#target_id
		#action_type
		#status hyperlink处理状态，1，待处理；2，处理中；3，处理完毕；
		#dc_status_code
		#dc_error_desc
		#upd_time
		#infiledate
		pass

	def toTuple(self):
		return (self.content_type,self.origin_id,self.provider_id,self.is_english,self.target_id,self.action_type,self.status,self.upd_time,self.infiledate)
