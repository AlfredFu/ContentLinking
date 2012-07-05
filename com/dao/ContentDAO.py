#coding=utf-8
from com.dao import *
from com.entity.Article import *

class ContentDAO(DAO):
	def __init__(self):
		super(ContentDAO,self).__init__()
		self.tableName='backup_content'

	def add(self,content,targetId,contentType):
		if content and targetId and contentType:
			content=self.escape_string(content)
			sql="Replace into %s(target_id,content_type,content,backup_time)values('%s','%s','%s',NOW());" %(self.tableName,targetId,contentType,content)
			try:
				self.cursor_stg.execute(sql)
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)

	def getByTarget(self,targetId,contentType):
		if targetId and contentType:
			sql="select content,target_id,content_type from %s where target_id='%s' and content_type='%s'" %(self.tableName,targetId,contentType)
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					return row[0]
			except Exception,e:
				self.log.error(e)
