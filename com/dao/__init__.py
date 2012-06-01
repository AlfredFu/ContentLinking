from com.util.DBConnUtil import *
from com.util.LogUtil import *

class DAO:
	def __init__(self):
		self.conn=DBConnUtil.getConnection()
        	self.cursor=self.conn.cursor()
		self.log=getLog()    
		self.conn_stg=DBConnUtil.getConnection('db_stg')
		self.cursor_stg=self.conn_stg.cursor()
		
		self.conn_hyperlink=DBConnUtil.getConnection('db_hyperlink')
		self.cursor_hyperlink=self.conn_hyperlink.cursor()
