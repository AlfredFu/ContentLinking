from com.entity.QueueItem import *
from com.dao import *

class HyperlinkQueueDAO(DAO):
	table='opr_load_status'

	def __init__(self):
		DAO.__init__(self)
		self.conn_stg=DBConnUtil.getConnection('db_stg')
		self.cursor_stg=self.conn_stg.cursor()
	
	def getAll(self):
		self.cursor_stg.execute("SELECT opr_id,content_type,origin_id,provider_id,is_english,target_id,action_type,status,dc_status_code,dc_error_desc,upd_time,infiledate FROM %s" % HyperlinkQueueDAO.table)	
		for row in self.cursor_stg.fetchall():
			queueItem=QueueItem()
			queueItem.id=row[0]
			queueItem.content_type=row[1]
			queueItem.origin_id=row[2]
			queueItem.provider_id=row[3]
			queueItem.is_english=row[4]
			queueItem.target_id=row[5]
			queueItem.action_type=row[6]
			queueItem.status=row[7]
			queueItem.upd_time=row[10]
			queueItem.infiledate=row[11]
			yield queueItem
			
	def add(self,queueItem):
		self.cursor_stg.execute("INSERT INTO %s (content_type,origin_id,provider_id,is_english,target_id,action_type,status,upd_time,infiledate ) values(%s,%s,%s,%s,%s,%s,%s)" % HyperlinkQueueDAO.table,queueItem.attrToTuple())
		self.conn_stg.commit()

	def initialQueue(self):
		pass
		
		
