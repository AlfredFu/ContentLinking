#coding=utf-8
from com.entity.Case import *
from com.dao import *
class CaseDAO(DAO):
	"case create,read,update and delete"
	
	def __init__(self):
		DAO.__init__(self)
	
	def getAll(self):
		"获取所有有效案例"
		try:
			self.cursor_stg.execute("SELECT case_id,title,origin_id,provider_id,isEnglish FROM cases WHERE isEnglish='Y' AND display=1;")
			for row in self.cursor_stg.fetchall():
				case=Case()
				case.id=row[0]
				case.title=row[1]
				case.originId=row[2]
				case.providerId=row[3]
				case.isEnglish=row[4]
				yield case	
		except Exception,e:
			self.log.error(e)

	def getById(self,id):
		"根据主键信息获取案例"
		if id:
			try:
				self.cursor_stg.execute("SELECT cases.case_id as id,cases.title,case_content.content,cases.origin_id,cases.provider_id,cases.isEnglish FROM cases LEFT JOIN case_content ON cases.case_id=case_content.case_id WHERE cases.case_id=%s;" % id)
				row=self.cursor_stg.fetchone()
				if row:
					article=Case()	
					article.id=row[0]
					article.title=row[1]
					article.content=row[2]
					article.originId=row[3]
					article.providerId=row[4]
					article.isEnglish=row[5]
					return article
				else:
					raise Exception("No case with id %s found!" %id)
			except Exception,e:
				self.log.error(e)	

	def getByOrigin(self,originId,providerId,isEnglish):
		"根据origin_id,provider_id,isEnglish获取案例"
		if originId and providerId and isEnglish:
			try:
				self.cursor_stg.execute("SELECT cases.case_id,cases.title,case_content.content FROM cases LEFT JOIN case_content ON cases.case_id=case_content.case_id WHERE cases.origin_id=%s AND cases.provider_id=%s AND cases.isEnglish='%s'" % (originId,providerId,isEnglish))
				row =self.cursor_stg.fetchone()
				case=Case()
				case.id=row[0]
				case.title=row[1]
				case.content=row[2]
				case.originId=originId
				case.providerId=providerId
				case.isEnglish=isEnglish
				return case	
			except Exception,e:
				self.log.error(e)

	def updateContent(self,article,isTransfer=False):
		"update content and in_time"
		if article:
			try:
				article.content=self.escape_string(article.content)
				sql="UPDATE case_content SET content='%s' WHERE case_id=%s" % (article.content,article.id)
				if isTransfer:
					self.cursor.execute(sql);
					self.conn.commit()
				else:
					self.cursor_stg.execute(sql);
					self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)

	def updateTime(self,article,isTransfer=False):
		if article:
			try:
				sql="UPDATE cases SET cases.in_time=NOW() WHERE case_id=%s" % article.id
				if isTransfer:
					self.cursor.execute(sql);
					self.conn.commit()
				else:
					self.cursor_stg.execute(sql);
					self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)

	def update(self,article,isTransfer=False):
		self.updateContent(article,isTransfer)
		self.updateTime(article,isTransfer)
		
if __name__=='__main__':
	caseDao=CaseDAO()
	for case in caseDao.getAll():
		print case.title
