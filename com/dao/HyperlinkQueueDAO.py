#coding=utf-8
from com.entity.QueueItem import *
from com.entity.Article import *
from com.dao import *

class HyperlinkQueueDAO(DAO):
	table='opr_load_status_en'

	def __init__(self):
		DAO.__init__(self)
	
	def getAll(self):
		try:
			self.cursor_stg.execute("SELECT opr_id,content_type,origin_id,provider_id,is_english,target_id,action_type,status,dc_status_code,dc_error_desc,upd_time,infiledate FROM %s where action_type in ('N','U','D') and status=1 order by content_type desc" % HyperlinkQueueDAO.table)	
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
			self.log.error(e)
			self.log.error("Error occured in getByContentType() of HyperlinkQueueDAO.py")
			
	def getByContentTypeStatus(self,contentType,status):
		"""
		Get hyperlink queue item by content type and status	
		param contentType 
		param status
		"""
		try:
			sql="SELECT opr_id,content_type,origin_id,provider_id,is_english,target_id,action_type,status,dc_status_code,dc_error_desc,upd_time,infiledate FROM %s where content_type='%s' and status=%s" % (HyperlinkQueueDAO.table,contentType,status)
			self.cursor_stg.execute(sql)
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
			self.log.error(e)
			self.log.error("Error occured in getByContentTypeStatus() of HyperlinkQueueDAO.py")
		
	def add(self,queueItem):
		try:
			sql="REPLACE INTO %s (content_type,origin_id,provider_id,is_english,target_id,action_type,status,upd_time,infiledate ) values(%s,%s,%s,%s,%s,%s,%s)" % ((HyperlinkQueueDAO.table,)+queueItem.toTuple())
			self.cursor_stg.execute(sql)
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)
			self.log.error(sql)

	def addMany(self,queueTupleList):
		try:
			self.cursor_stg.executemany("INSERT INTO "+HyperlinkQueueDAO.table+" (content_type,origin_id,provider_id,is_english,target_id,action_type,status,upd_time,infiledate ) values(%s,%s,%s,%s,%s,%s,%s,NOW(),CURDATE())" ,queueTupleList)
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)
		

	def updateActionType(self,targetId,contentType,actionType):
		if targetId and contentType and actionType:
			try:
				self.cursor_stg.execute("UPDATE opr_load_status_en SET action_type='%s' WHERE target_id=%s AND content_type='%s'" % (actionType,targetId,contentType))
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)

	def addAllToQueue(self):
		try:
			sql="UPDATE opr_load_status_en SET status=1 WHERE status=11;"
			self.cursor_stg.execute(sql)
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)

	def updateStatus(self,targetId,contentType,status):
		"""
		更新hyperlink队列中谋篇文章的hyperlink状态
		"""
		if targetId and contentType and status:
			try:
				self.cursor_stg.execute("update opr_load_status_en set status=%s where target_id='%s' and content_type='%s';" %(status,targetId,contentType))
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)

	def rollbackToStatus(self,targetId,contentType,status=Article.STATUS_FINISHED,toStatus=Article.STATUS_WAIT_UPLOAD):
		"""
		将队列中的文章A(由targetId,contentType指定)的状态由status改为toStatus
		"""
		if targetId and contentType:
			sql="update opr_load_status_en set status=%s where target_id=%s and content_type='%s' and status=%s;" %(toStatus,targetId,contentType,status)
			try:
				self.cursor_stg.execute(sql)
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)
		
	def updateActionType(self,targetId,contentType,actionType):
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
