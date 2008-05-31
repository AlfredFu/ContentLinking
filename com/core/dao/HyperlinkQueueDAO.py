from com.core.entity.Keyword import *
from com.core.dao import *

class HyperlinkQueueDAO(DAO):
	table='opr_load_status'

	def __init__(self):
		DAO.__init__(self)
		self.conn_stg=DBConnUtil.getConnection('db_stg')
		sele.cursor_stg=self.conn_stg.cursor()
	
	def getAll(self):
		self.cursor_stg.execute("SELECT content_type,origin_id,provider_id,is_english,target_id,action_type,status,dc_status_code,dc_error_desc,upd_time,infiledate FROM %s" % HyperlinkQueueDAO.table)	
	def add(self,queueItem):
		for row in self.cursor_stg.fetchall():
			yield row['origin_id'}

	def initialQueue(self):
		
