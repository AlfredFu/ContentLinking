from com.util.DBConnUtil import *
from com.util.LogUtil import *
import MySQLdb

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

	def escape_string(self,str):
		if str:
			return MySQLdb.escape_string(str)

if __name__=="__main__":
	dao=DAO()
	print dao.escape_string("People's")
