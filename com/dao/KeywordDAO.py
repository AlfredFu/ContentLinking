#coding=utf-8
from com.entity.Keyword import *
from com.dao import *

class KeywordDAO(DAO):
	table='keyword_en'
        rep="of the People's Republic of China"
	
	def __init__(self):
		super(KeywordDAO,self).__init__()
		self.cursor_hyperlink.execute("use lnc;")

	def add(self,keyword):
		try:
			keyword.content=keyword.content.replace("'","\\'")
			keyword.content=keyword.content.replace('"','\\"')
			if not keyword.fullTitleKeywordId:
				self.cursor_hyperlink.execute("replace into keyword_en(keyword,status,type) values('%s','NOR','%s')" % (keyword.content,keyword.type))
			else:
				self.cursor_hyperlink.execute("replace into keyword_en(keyword,status,type,full_title_keyword_id) values('%s','NOR','%s',%s)" % (keyword.content,keyword.type,keyword.fullTitleKeywordId))
            		self.conn_hyperlink.commit()
			return self.cursor_hyperlink.lastrowid
		except Exception,e:
			self.log.error(e)
	
	def deleteByTarget(self,targetId,contentType):
		pass

    	def getAll(self):
		try:
			self.cursor_hyperlink.execute("select keyword_id,keyword,status,type,full_title_keyword_id from %s ORDER BY LENGTH(keyword) DESC" % KeywordDAO.table )
        		for row in self.cursor_hyperlink.fetchall():
            			yield self.assembleKeyword(row)
		except Exception,e:
			self.log.error(e)

    	def getById(self,id):
        	try:
             		self.cursor.execute("select keyword_id,keyword,status,type,full_title_keyword_id from %s where keyword_id=%s" % (table,id))
			row =self.cursor.fetchone()
			return self.assembleKeyword(row)
		except Exception,e:
	     		self.log.error(e)

	def getFullTitleKeyword(self,id):
		try:
			self.cursor.execute("select keyword_id,keyword,status,type,full_title_keyword_id from %s where keyword_id=(select full_title_keyword_id from %s where keyword_id=%s)" % (KeywordDAO.table,KeywordDAO.table,id))
			row=self.cursor.fetchone()
			return keyword
		except Exception,e:
			self.log.error(e)

	def findByContent(self,content):
		"""
		根据关键词内容找到关键词
		"""
		try:
			self.cursor_hyperlink.execute("select keyword_id,keyword,status,type,full_title_keyword_id,removed_record_id,isenabling from keyword_en where keyword='%s'" % content.replace("'","\\'"))
			row=self.cursor_hyperlink.fetchone()
			if row:
				keyword=self.assembleKeyword(row)
				return keyword
		except Exception,e:
			self.log.error(e)

	def assembleKeyword(self,row):
		keyword=Keyword()
		keyword.id=row[0]
		keyword.content=row[1]
		keyword.status=row[2]
		keyword.type=row[3]
            	keyword.fullTitleKeywordId=row[4]
		return keyword
		
if __name__=='__main__':
    keywordDAO=KeywordDAO()
    for keyword in keywordDAO.getAll():
        print keyword.content
