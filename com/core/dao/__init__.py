from com.util.DBConnUtil import *
from com.util.LogUtil import *

class DAO:
	def __init__(self):
		self.conn=DBConnUtil.getConnection()
        	self.cursor=self.conn.cursor()
		self.log=getLog()    
