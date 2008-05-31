from com.entity.Case import *
from com.dao import *

class CaseDAO(DAO):
	"case create,read,update and delete"
	
	def __init__(self):
		DAO.__init__(self)
		self.conn_stg=DBConnUtil.getConnection('db_stg')
		self.cursor_stg=self.conn_stg.cursor()
	
	def getCase(self):
		self.cursor_stg.execute("SELECT case_id,title,origin_id,provider_id,isEnglish FROM cases WHERE display=1;")
		for row in self.cursor_stg.fetchall():
			case=Case()
			case.id=row[0]
			case.title=row[1]
			case.originId=row[2]
			case.providerId=row[3]
			case.isEnglish=row[4]
			yield case	

	def getFullCaseByPrimaryKey(self,originId,providerId,isEnglish):
		self.cursor_stg.execute("SELECT cases.case_id,title,content")