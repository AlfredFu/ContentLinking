from com.dao import *

class LawDAO(DAO):
	def __init__(self):
		DAO.__init__(self)
	
	def getLawByKeywordId(self,keywordId):
		self.cursor_hyperlink.execute("SELECT origin_id,provider_id,isEnglish,target_id,action_type,status,keyword_id FROM article WHERE keyword_id='%s'" % keywordId)
		return self.cursor_hyperlink.fetchall()

	def update(self,article):
		self.cursor_stg.execute("UPDATE tax_content SET content='%s' WHERE origin_id=%s AND provider_id=%s AND isEnglish='%s'" % (article.content,article.originId,article.providerId,article.isEnglish))
		self.updateTime(article)	

	def updateTime(self,article):
		self.cursor_stg.execute("UPDATE tax SET indbtime=NOW() WHERE origin_id=%s AND provider_id=%s AND isEnglish='%s';" % (article.origin_id,article.provider_id,article.isEnglish));

	def updateTimeByPrimary(self,id):
		self.cursor_stg.execute("UPDATE tax SET indbtime=NOW() WHERE taxid=%s;" % id) 
		
	def getLawByKeywordId(self,keywordId):
		self.cursor_hyperlink.execute("SELECT origin_id,provider_id,isEnglish,target_id,action_type FROM article WHERE keyword_id=%s AND content_type='T';" % keywordId)
		return self.cursor_hyperlink.fetchall()	
	def getLawById(self,id):
		self.cusor_stg.execute("")
			
if __name__ =="__main__":
	lawDAO=LawDAO()
	print lawDAO.getLawByKeywordId(2505)
