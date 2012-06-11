#coding=utf-8
from com.entity.Keyword import *
from com.dao import *

class KeywordDAO(DAO):
	table='keyword_en'
        rep="of the People's Republic of China"
	
	def __init__(self):
		super(KeywordDAO,self).__init__()

    	def getAll(self):
		self.cursor.execute("select keyword_id,keyword,status,type,full_title_keyword_id from %s ORDER BY LENGTH(keyword) DESC" % KeywordDAO.table )
        	for row in self.cursor.fetchall():
            		yield self.assembleKeyword(row)

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
        
    	def initialKeyword(self):
        	self.cursor.execute('set names GBK;')
        	self.cursor.execute('use newlaw;')
        	keywordInitialSql="select title from tax where isEnglish='Y' and display=1 and duplicate_flag=0;"
        	self.cursor.execute(keywordInitialSql)
        	keywordsEn=[]
        	try:
			row=self.cursor.fetchone()
            		while row:
                		keywordsEn.append((row[0],'F'))
                		if rep in row[0]:
                    			keywordsEn.append((row[0].replace(rep,''),'A'))
                	row=self.cursor.fetchone()
            		self.cursor.execute('use lnc;')
            		self.cursor.execute('delete from %s' % table)
            		self.conn.commit()
            		self.cursor.executemany("insert into keyword_en(keyword,status,type) values(%s,'NOR',%s)",keywordsEn)
            		self.conn.commit()
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
