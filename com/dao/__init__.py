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
		Get article in whose content contain ltext
		"""
		if ltext:
			try:
				sql="select origin_id,provider_id,isEnglish from "+self.contentTable+" where isEnglish='Y' and content like '%"+self.escape_string(ltext)+"%'"
				self.cursor_stg.execute(sql)
				for row in self.cursor_stg.fetchall():
					yield (row[0],row[1],row[2])
			except Exception,e:
				self.log.error(e)
			

	def escape_string(self,str):
		return escapeString(str)#function escapeStirng defined in DBConnUtil

if __name__=="__main__":
	print escapeString("People's")
