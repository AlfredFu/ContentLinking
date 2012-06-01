from com.entity.QueueItem import *
from com.dao import *

class HyperlinkQueueDAO(DAO):
	table='opr_load_status_en'

	def __init__(self):
		DAO.__init__(self)
	
	def getAll(self):
		self.cursor_stg.execute("SELECT opr_id,content_type,origin_id,provider_id,is_english,target_id,action_type,status,dc_status_code,dc_error_desc,upd_time,infiledate FROM %s" % HyperlinkQueueDAO.table)	
		for row in self.cursor_stg.fetchall():
			queueItem=QueueItem()
			queueItem.id=row[0]
			queueItem.contentType=row[1]
			queueItem.originId=row[2]
			queueItem.providerId=row[3]
			queueItem.isEnglish=row[4]
			queueItem.targetId=row[5]
			queueItem.actionType=row[6]
			queueItem.status=row[7]
			queueItem.updTime=row[10]
			queueItem.infiledate=row[11]
			yield queueItem
			
	def add(self,queueItem):
		self.cursor_stg.execute("INSERT INTO %s (content_type,origin_id,provider_id,is_english,target_id,action_type,status,upd_time,infiledate ) values(%s,%s,%s,%s,%s,%s,%s)" % HyperlinkQueueDAO.table,queueItem.attrToTuple())
		self.conn_stg.commit()

	def addMany(self,queueTupleList):
		self.cursor_stg.executemany("INSERT INTO "+HyperlinkQueueDAO.table+" (content_type,origin_id,provider_id,is_english,target_id,action_type,status,upd_time,infiledate ) values(%s,%s,%s,%s,%s,%s,%s,NOW(),CURDATE())" ,queueTupleList)
		self.conn_stg.commit()


			
if __name__ =="__main__":
	dao=HyperlinkQueueDAO()
	for queueItem in dao.getAll():
		print queueItem
