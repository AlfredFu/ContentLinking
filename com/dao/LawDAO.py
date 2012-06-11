from com.dao import *
from com.entity.Law import *

class LawDAO(DAO):
	def __init__(self):
		DAO.__init__(self)
	

	def update(self,article):
		self.cursor_stg.execute("UPDATE tax_content SET content='%s' WHERE origin_id=%s AND provider_id=%s AND isEnglish='%s'" % (article.content,article.originId,article.providerId,article.isEnglish))
		self.updateTime(article)	

	def updateTime(self,article):
		self.cursor_stg.execute("UPDATE tax SET indbtime=NOW() WHERE origin_id=%s AND provider_id=%s AND isEnglish='%s';" % (article.origin_id,article.provider_id,article.isEnglish));

	def updateTimeByPrimary(self,id):
		self.cursor_stg.execute("UPDATE tax SET indbtime=NOW() WHERE taxid=%s;" % id) 
		
	def getLawByKeywordId(self,keywordId):
		self.cursor_hyperlink.execute("SELECT origin_id,provider_id,isEnglish,target_id,action_type FROM article WHERE keyword_id=%s AND content_type='T';" % keywordId)
		articleList=[]
		for row in self.cursor_hyperlink.fetchall():
			article=Law()
			article.originId=row[0]
			article.providerId=row[1]
			article.isEnglish=row[2]
			article.targetId=row[3]
			article.id=row[3]
			article.actionType=row[4]
			articleList.append(article)
		#return self.cursor_hyperlink.fetchall()	
		return articleList
	
	def getById(self,id):
		article=Law()	
		try:
			self.cusor_stg.execute("SELECT tax.taxid as id,tax.title,tax_content.content FROM tax LEFT JOIN tax_content ON tax.taxid=tax_content.taxid WHERE tax.taxid=%s;" % id)
			row=self.cursor_stg.fetchone()
			if row:
				article.id=row[0]
				article.title=row[1]
				article.content=row[2]
			else:
				raise Exception("No law with id %s found!" %id)
		except Exception,e:
			self.log.error(e)	
		return article
if __name__ =="__main__":
	lawDAO=LawDAO()
	print lawDAO.getLawByKeywordId(2505)
