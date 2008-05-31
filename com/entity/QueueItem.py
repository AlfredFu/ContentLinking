class QueueItem:
	
	def __init__(self):
		#opr_id
		#content_type
		#origin_id
		#provider_id
		#is_english
		#target_id
		#action_type
		#status
		#dc_status_code
		#dc_error_desc
		#upd_time
		#infiledate
		pass

	def attrToTuple(self):
		return (self.content_type,self.origin_id,self.provider_id,self.is_english,self.target_id,self.action_type,self.status,self.upd_time,self.infiledate)
