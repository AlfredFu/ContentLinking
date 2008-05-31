from com.core.entity.Keyword import *
from com.core.dao import *
class HyperlinkQueueDAO(DAO):
	table='opr_load_status'

	def __init__(self):
		DAO.__init__(self)
		self.conn=DBConnUtil.getConnection('db_stg')
		sele.cursor=DB
	
	def getAll(self):
		pass
	

	def initialQueue(self):
		
