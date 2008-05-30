from com.core.entity.Keyword import *
from com.core.dao import *
class HyperlinkQueueDAO(DAO):
	table='opr_load_status'

	def __init__(self):
		DAO.__init__(self)
		self.cursor.execute('use lnc;')
