#coding=utf-8
from com.entity.Version import *
from com.dao import *

class VersionDAO(DAO):
	"""
	法规版本参考，数据库操作接口	
	"""

	def __init__(self):
		super(VersionDAO,self).__init__()

	def add(self,version):
		pass

	def addMany(self,versionList):
		tupleList=[]
		for version in versionList:
			tupleList.append(version.toTuple())
		try:
			#TODO optimize
			#self.cursor.executemany("replace into versions(src_origin_id,src_provider_id,src_isenglish,des_origin_id,des_provider_id,des_isenglish) values('%s',%s,'%s','%s',%s,'%s')",tupleList)
			for tuple in tupleList:
				self.cursor_stg.execute("replace into versions(src_origin_id,src_provider_id,src_isenglish,des_origin_id,des_provider_id,des_isenglish) values('%s',%s,'%s','%s',%s,'%s')" % tuple)
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)

	def deleteByOrigin(self,originId,providerId,isEnglish):
		try:
			self.cursor_stg.execute("DELETE FROM versions WHERE (src_origin_id='%s' and src_provider_id=%s and src_isenglish='%s') or (des_origin_id='%s' and des_provider_id=%s and des_isenglish='%s')" %(originId,providerId,isEnglish,originId,providerId,isEnglish))
			self.conn_stg.commit()
		except Exception,e:
			self.log.error(e)

	def deleteBySrc(self,srcOriginId,srcProviderId,srcIsEnglish):
		pass

	def deleteByDes(self,desOriginId,desProviderId,desIsEnglish):
		pass

	def deleteBySrcDes(self):
		pass
