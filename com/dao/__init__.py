from com.util.DBConnUtil import *
from com.util.LogUtil import *

class DAO(object):
	def __init__(self):
		self.conn=DBConnUtil.getConnection()
        	self.cursor=self.conn.cursor()
		self.cursor.execute("USE newlaw;")

		self.conn_stg=DBConnUtil.getConnection('db_stg')
		self.cursor_stg=self.conn_stg.cursor()
		
		self.conn_hyperlink=DBConnUtil.getConnection('db_hyperlink')
		self.cursor_hyperlink=self.conn_hyperlink.cursor()
		
		self.log=getLog()    

	def getArticleContainText(self,ltext):
		"""
		"""
		if ltext:
			sql="select from "+self.table+" where content like '%"+ltext+"%'"
			

	def escape_string(self,str):
		return escapeString(str)#function escapeStirng defined in DBConnUtil

if __name__=="__main__":
	print escapeString("People's")
