#coding=utf-8
from com.dao import *
from com.entity.Law import *
import sys

class LawDAO(DAO):
	def __init__(self):
		DAO.__init__(self)
		self.contentTable="tax_content"
	
	def getAll(self):
		try:
			self.cursor_stg.execute("select taxid,title,origin_id,provider_id,isEnglish from tax where isEnglish='Y' and display=1 and duplicate_flag=0")
			for row in self.cursor_stg.fetchall():
				law=Law()
				law.id=row[0]
				law.title=row[1]
				law.originId=row[2]
				law.providerId=row[3]
				law.isEnglish=row[4]
				yield law
		except Exception,e:
			self.log.error(e)

	def update(self,article,isTransfer=False):
		if article.originId and article.providerId and article.isEnglish and article.content:
			article.content=self.escape_string(article.content)
			sql="UPDATE tax_content SET content='%s' WHERE origin_id='%s' AND provider_id=%s AND isEnglish='%s'" % (article.content,article.originId,article.providerId,article.isEnglish)
			try:
				if isTransfer:
					self.cursor.execute(sql)
					self.conn.commit()
				else:
					self.cursor_stg.execute(sql)
					self.conn_stg.commit()
				self.updateTime(article,isTransfer)	
			except Exception,e:
				self.log.error(e)

	def updateTime(self,article,isTransfer=False):
		if article.originId and article.providerId and article.isEnglish:
			sql="UPDATE tax SET indbtime=NOW() WHERE origin_id='%s' AND provider_id=%s AND isEnglish='%s';" % (article.originId,article.providerId,article.isEnglish)
			try:
				if isTransfer:
					self.cursor.execute(sql);
					self.conn.commit()
				else:
					self.cursor_stg.execute(sql);
					self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)

	def updateTimeByPrimary(self,id):
		if id:
			try:
				self.cursor_stg.execute("UPDATE tax SET indbtime=NOW() WHERE taxid=%s;" % id) 
				self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)
		
	def getLawByKeywordId(self,keywordId):
		if keywordId:
			try:
				self.cursor_hyperlink.execute("SELECT origin_id,provider_id,isEnglish,target_id,action_type FROM article_en WHERE keyword_id=%s AND content_type='T' ORDER BY provider_id asc;" % keywordId)
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
				return articleList
			except Exception,e:
				self.log.error(e)
	
	def getById(self,id):
		if id:
			try:
				
				self.cursor_stg.execute("SELECT tax.taxid as id,tax.title,tax_content.content,tax.origin_id,tax.provider_id,tax.isEnglish,tax.date,tax.effect_date FROM tax LEFT JOIN tax_content ON tax.taxid=tax_content.taxid WHERE tax.taxid=%s;" % id)
				row=self.cursor_stg.fetchone()
				if row:
					article=Law()	
					article.id=row[0]
					article.title=row[1]
					article.content=row[2]
					article.originId=row[3]
					article.providerId=row[4]
					article.isEnglish=row[5]
					article.proDate=row[6]
					article.effectDate=row[7]
					return article
				else:
					raise Exception("No law with id %s found!" %id)
			except Exception,e:
				self.log.error(e)	
	
	def getByOrigin(self,originId,providerId,isEnglish):
		"""
		根据originId,providerId,isEnglish获取法规
		"""
		article=Law()	
		try:
			self.cursor_stg.execute("SELECT tax.taxid as id,tax.title,tax_content.content,tax.origin_id,tax.provider_id,tax.isEnglish,tax.date,tax.effect_date FROM tax LEFT JOIN tax_content ON tax.taxid=tax_content.taxid WHERE tax.origin_id='%s' and tax.provider_id=%s and tax.isEnglish='%s' and display=1;" % (originId,providerId,isEnglish))
			row=self.cursor_stg.fetchone()
			if row:
				article.id=row[0]
				article.title=row[1]
				article.content=row[2]
				article.originId=row[3]
				article.providerId=row[4]
				article.isEnglish=row[5]
				article.proDate=row[6]
				article.effectDate=row[7]
			else:
				raise Exception("No law with origin_id:%s,provider_id:%s,isEnglish:%s found!" %(originId,providerId,isEnglish))
		except Exception,e:
			self.log.error(e)	
			self.log.error("getByOrigin in LawDAO.py")
		return article

	def getArticleContainText(self,ltext):
		for row in super(LawDAO,self).getArticleContainText(ltext):
			yield(row[0],row[1],row[2],Article.CONTENT_TYPE_LAW)
