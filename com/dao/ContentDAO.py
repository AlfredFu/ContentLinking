#coding=utf-8
from com.dao import *
from com.entity.Article import *

class ContentDAO(DAO):
	def __init__(self):
		super(ContentDAO,self).__init__()

	def add(self,content,targetId,contentType):
		pass	

	def getByTarget(self,targetId,contentType):
		pass

