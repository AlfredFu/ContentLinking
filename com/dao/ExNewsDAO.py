#coding=utf-8
from com.entity.Article import *
from com.dao import *

class ExNewsDAO(DAO):
	"""
	操作数据库ex_news表接口
	"""

	def __init__(self):
		super(ExNewsDAO,self).__init__()

	def getAll(self):
		"""
		
		"""
		try:
			sql="select ex_news.id,ex_news.title,ex_news.origin_id,ex_news.provider_id,ex_news.isEnglish,ex_news_contents.content,ex_news.sub_type,ex_news.type,ex_news.alltype,ex_news.ipnews_category,ex_news.promulgation_date from ex_news left join ex_news_contents on ex_news.id=ex_news_contents.ex_new_id where ex_news.isEnglish='Y' and ex_news.is_display=1;" 
			self.cursor_stg.execute(sql)
			for row in self.cursor_stg.fetchall():
				for article in self.generatorAssemble(row):
					if article.contentType != Article.CONTENT_TYPE_OTHERS:
						yield article 
		except Exception,e:
			self.log.error(e)

	def getById(self,id):
		if id:
			sql="select ex_news.id,ex_news.title,ex_news.origin_id,ex_news.provider_id,ex_news.isEnglish,ex_news_contents.content,ex_news.sub_type,ex_news.type,ex_news.alltype,ex_news.ipnews_category,ex_news.promulgation_date from ex_news left join ex_news_contents on ex_news.id=ex_news_contents.ex_new_id where ex_news.id=%s" % id
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					article=self.assemble(row)
					return article
				else:
					raise Exception("No article with id:%s in table ex_news is found!" % id)
			except Exception,e:
				self.log.error(e)

	def getByOrigin(self,originId,providerId,isEnglish):
		if originId and providerId and isEnglish:
			sql="select ex_news.id,ex_news.title,ex_news.origin_id,ex_news.provider_id,ex_news.isEnglish,ex_news_contents.content,ex_news.sub_type,ex_news.type,ex_news.alltype,ex_news.ipnews_category,ex_news.promulgation_date from ex_news left join ex_news_contents on ex_news.id=ex_news_contents.ex_new_id where ex_news.origin_id='%s' and ex_news.provider_id=%s and ex_news.isEnglish='%s';" % (originId,providerId,isEnglish) 
			try:
				self.cursor_stg.execute(sql)
				row=self.cursor_stg.fetchone()
				if row:
					article=self.assemble(row)
					return article
				else:
					raise Exception("No article with origin_id:%s,provider_id:%s,isEnglish:%s is found in table ex_news!" %(originId,providerId,isEnglish))
			except Exception,e:
				self.log.error(e)


	def update(self,article,isTransfer=False):
		if article and article.id and article.content is not None:
			article.content=self.escape_string(article.content)
			updateTimeSql="update ex_news set update_time=NOW() where id=%s;" % article.id	
			updateContentSql="update ex_news_contents set content='%s' where ex_new_id=%s" % (article.content,article.id)
			try:
				if isTransfer:
					self.cursor.execute(updateTimeSql)
					self.cursor.execute(updateContentSql)
					self.conn.commit()
				else:
					self.cursor_stg.execute(updateTimeSql)
					self.cursor_stg.execute(updateContentSql)
					self.conn_stg.commit()
			except Exception,e:
				self.log.error(e)
		else:
			self.log.warning("No Illegal article")
	
	def generatorAssemble(self,row):
		if row:
			article=Article()
			article.id=row[0]
			article.title=row[1]
			article.originId=row[2]
			article.providerId=row[3]
			article.isEnglish=row[4]
			article.content=row[5]
			article.subType=row[6]
			article.type=row[7]
			article.allType=row[8]
			article.ipnewsCategory=row[9]
			article.proDate=row[10]
			if article.subType == 1:
				article.contentType=Article.CONTENT_TYPE_NEWLAW#每日快讯(新法快报)
				yield article
			elif article.subType==3 and article.ipnewsCategory==1:
				article.contentType=Article.CONTENT_TYPE_HOTNEWS#评论文章
				yield article
			elif article.subType==4:
				article.contentType=Article.CONTENT_TYPE_PRACTICAL#实用资料
				yield article
			elif article.subType==6:
				article.contentType=Article.CONTENT_TYPE_ELEARNING#在线培训
				yield article
			elif article.subType==7:
				overviewType={'2':Article.CONTENT_TYPE_IPOVERVIEW,'3':Article.CONTENT_TYPE_EPOVERVIEW,'4':Article.CONTENT_TYPE_CPOVERVIEW,'5':Article.CONTENT_TYPE_TPOVERVIEW,'6':Article.CONTENT_TYPE_FDIOVERVIEW,'7':Article.CONTENT_TYPE_EEOVERVIEW,'8':Article.CONTENT_TYPE_CSOVERVIEW}
				for topicId in article.allType.split(','):
					article.contentType=overviewType[topicId]
					yield article
			else:
				article.contentType=Article.CONTENT_TYPE_OTHERS
				yield article
			
        def assemble(self,row):
                if row:
                        article=Article()
                        article.id=row[0]
                        article.title=row[1]
                        article.originId=row[2]
                        article.providerId=row[3]
                        article.isEnglish=row[4]
                        article.content=row[5]
                        article.subType=row[6]
                        article.type=row[7]
                        article.allType=row[8]
                        article.ipnewsCategory=row[9]
			article.proDate=row[10]
                        if article.subType == 1:
                                article.contentType=Article.CONTENT_TYPE_NEWLAW#每日快讯(新法快报)
                        elif article.subType==3 and article.ipnewsCategory==1:
                                article.contentType=Article.CONTENT_TYPE_HOTNEWS#评论文章
                        elif article.subType==4:
                                article.contentType=Article.CONTENT_TYPE_PRACTICAL#实用资料
                        elif article.subType==6:
                                article.contentType=Article.CONTENT_TYPE_ELEARNING#在线培训
                        elif article.subType==7:
                                article.contentType=Article.CONTENT_TYPE_TPOVERVIEW
                        else:
                                article.contentType=Article.CONTENT_TYPE_OTHERS
                        return article


	def getByContentType(self,contentType):
		pass

if __name__=='__main__':
	dao=ExNewsDAO()
	article=dao.getById(156)
	print article.title
