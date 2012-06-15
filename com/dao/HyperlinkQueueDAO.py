#coding=utf-8
from com.entity.QueueItem import *
from com.dao import *

class HyperlinkQueueDAO(DAO):
	table='opr_load_status_en'

	def __init__(self):
		DAO.__init__(self)
	
	def getAll(self):
		try:
			self.cursor_stg.execute("SELECT opr_id,content_type,origin_id,provider_id,is_english,target_id,action_type,status,dc_status_code,dc_error_desc,upd_time,infiledate FROM %s where action_type in ('N','U','D') and status=1" % HyperlinkQueueDAO.table)	
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
		except Exception,e:
			print e
			self.log.error(e)
			
	def getByContentType(self,contentType=''):
		try:
			self.cursor_stg.execute("SELECT opr_id,content_type,origin_id,provider_id,is_english,target_id,action_type,status,dc_status_code,dc_error_desc,upd_time,infiledate FROM %s where status=1 and content_type='%s'" % (HyperlinkQueueDAO.table,contentType))	
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
		except Exception,e:
			print e
			self.log.error(e)
			
	def add(self,queueItem):
		self.cursor_stg.execute("INSERT INTO %s (content_type,origin_id,provider_id,is_english,target_id,action_type,status,upd_time,infiledate ) values(%s,%s,%s,%s,%s,%s,%s)" % HyperlinkQueueDAO.table,queueItem.attrToTuple())
		self.conn_stg.commit()

	def addMany(self,queueTupleList):
		self.cursor_stg.executemany("INSERT INTO "+HyperlinkQueueDAO.table+" (content_type,origin_id,provider_id,is_english,target_id,action_type,status,upd_time,infiledate ) values(%s,%s,%s,%s,%s,%s,%s,NOW(),CURDATE())" ,queueTupleList)
		self.conn_stg.commit()

	def updateActionType(self,id,type):
		try:
			self.cursor_stg.execute("UPDATE opr_load_status SET action_type='%s' WHERE target_id=%s AND action_type=''" % (type,id))
			self.conn_stg.commit()
		except Exception,e:
			print e
			self.log.error(e)

	def addAllToQueue(self):
		try:
			self.cursor_stg.execute("UPDATE opr_load_status SET action_type='U' WHERE action_type=''")
		except Exception,e:
			print e
			self.log.error(e)

	def updateStatus(self,targetId,status,contentType):
		"""
		更新hyperlink队列中谋篇文章的hyperlink状态
		"""
		try:
			self.cursor_stg.execute("update opr_load_status_en set status=%s where target_id='%s' and content_type='%s'" %(status,targetId,contentType))
			self.conn_stg.commit()
		except Exception,e:
			print e
			self.log.error(e)

	def updateActionType(self,targetId,actionType,contentType):
		"""
		更新队列中某篇文章的状态
		"""
		try:
			self.cursor_stg.execute("update opr_load_status_en set action_type='%s' where target_id='%s' and content_type='%s'" % (actionType,targetId,contentType))
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)
			self.log.error("Error occured in updateActionType of HyperlinkQueueDAO")
			
if __name__ =="__main__":
	dao=HyperlinkQueueDAO()
	for queueItem in dao.getAll():
		print queueItem
