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
			self.cursor_stg.execute("SELECT opr_id,content_type,origin_id,provider_id,is_english,target_id,action_type,status,dc_status_code,dc_error_desc,upd_time,infiledate FROM %s where action_type in ('N','U','D') and status=1 order by content_type asc" % HyperlinkQueueDAO.table)	
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
			
	def getByStatus(self,status=Article.STATUS_WAIT_UPLOAD):
		try:
			self.cursor_stg.execute("SELECT opr_id,content_type,origin_id,provider_id,is_english,target_id,action_type,status,dc_status_code,dc_error_desc,upd_time,infiledate FROM %s where action_type in ('N','U','D') and status=%s order by content_type asc" % (HyperlinkQueueDAO.table,status))	
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
			
	def getByContentTypeStatus(self,contentType,status,actionType=''):
		"""
		Get hyperlink queue item by content type and status	
		param contentType 
		param status
		"""
		try:
			if actionType:
				sql="SELECT opr_id,content_type,origin_id,provider_id,is_english,target_id,action_type,status,dc_status_code,dc_error_desc,upd_time,infiledate FROM %s where content_type='%s' and status=%s and action_type='%s';" % (HyperlinkQueueDAO.table,contentType,status,actionType)
			else:
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

	def getByTargetIdContentType(self,targetId,contentType,isEnglish='Y'):
		try:
			if targetId and contentType and isEnglish:
				sql="SELECT opr_id,content_type,origin_id,provider_id,is_english,target_id,action_type,status,\
					dc_status_code,dc_error_desc,upd_time,infiledate FROM %s \
					where  target_id=%s and content_type='%s' and is_english='%s';" \
					% (HyperlinkQueueDAO.table,targetId,contentType,isEnglish)
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
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
					return queueItem
		except Exception,e:
			self.log.error(e)
		
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
		"""
		Change article's status in queue from 11 to 1 when article's action_type is 'U' or 'N',
		Article's action_type have to be changed from 'N' to 'U'
		"""
		try:
			sql="UPDATE opr_load_status_en SET status=1,action_type='U' WHERE action_type in ('N','U') and status=11;"
			self.cursor_stg.execute(sql)
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)

	def addToQueue(self,tupleList):
		"""
		Change article's status in queue from 11 to 1 when article's action_type is 'U' or 'N',
		Article's action_type have to be changed from 'N' to 'U'
		"""
		sql=''
		for originTuple in tupleList:
			originId=originTuple[0]
			providerId=originTuple[1]
			isEnglish=originTuple[2]
			contentType=originTuple[3]
			if originId and providerId and isEnglish and contentType:
				sql="UPDATE opr_load_status_en SET status=1,action_type='U' \
					WHERE origin_id='%s' and provider_id=%d and is_english='%s' \
					and content_type='%s' and  action_type in ('N','U') and status=11;" \
					%(originId,providerId,isEnglish,contentType)
				try:
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

	def updateStatusActionType(self,targetId,contentType,status,actionType='U'):
		"""
		更新hyperlink队列中谋篇文章的hyperlink状态
		"""
		if targetId and contentType and status and actionType:
			try:
				self.cursor_stg.execute("update opr_load_status_en set status=%s,action_type='%s' where target_id=%s and content_type='%s';" %(status,actionType,targetId,contentType))
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

	def updateQueueStatus(self,fromStatus,toStatus):
		if fromStatus and toStatus:
			sql="update opr_load_status_en set status=%s where status=%s" %(toStatus,fromStatus) 		
			try:
				self.cursor_stg.execute(sql)
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)
	
	def updateTargetArticleStatus(self,targetId,contentType,toStatus=Article.STATUS_WAIT_UPLOAD,fromStatus=Article.STATUS_FINISHED):
		"""
		用于将被引用但未在当前队列被处理的法规加入到，法条被引用信息统计处理列表	
		"""
		if targetId and contentType and toStatus and fromStatus:
			sql="update opr_load_status_en set status=%s where target_id=%s and content_type='%s' and status=%s and action_type<>'D';" %(toStatus,targetId,contentType,fromStatus)
			try:
				self.cursor_stg.execute(sql)
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)
			

	def collectStatisticsOfProcessedData(status=Article.STATUS_WAIT_UPLOAD):
		"""
		统计本次hyperlink所处理的数据，如处理了多少条新增的，多少条修改的，多少删除的以及各种内容类型的情况
		(必须在数据处理完但未上传时统计才有效)
		"""
		if status:
			sql1="SELECT action_type,COUNT(*) FROM opr_load_status_en WHERE status=%s GROUP BY action_type" % status#按处理方式统计
			sql2="SELECT content_type,COUNT(*) FROM opr_load_status_en WHERE status=%s GROUP BY content_type" % status#按内容类型统计
			try:
				self.cursor_stg.execute(sql1)
				for row in self.cursor_stg.fetchall():
					yield (row[0],row[1],'BY_ACTION')#BY_ACTION标记这条数据是根基action_type统计出来的

				self.cursor_stg.execute(sql2)
				for row in self.cursor_stg.fetchall():
					yield (row[0],row[1],'BY_CONTENT')#BY_CONTENT标记这条数据是根据内容类型统计出来的
			except Exception,e:
				self.log.error(e)

		
		
if __name__ =="__main__":
	dao=HyperlinkQueueDAO()
	for queueItem in dao.getAll():
		print queueItem
