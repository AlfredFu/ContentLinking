#!/usr/bin/env python
# coding=utf-8
import sys
sys.path.append("/home/fred/workspace/EnglishHyperlink")
from com.process import *

class FindLaw(HyperlinkProcess):
        def __init__(self):
                super(FindLaw,self).__init__()  

        def findIllegal(self):
                for row in self.lawDao.getAll():
                        law=self.lawDao.getByOrigin(row.originId,row.providerId,row.isEnglish)  
                        if law and law.content:
                                 if self.oldProvisionPosTagPattern.search(law.content):
                                        print law.originId,law.providerId,law.isEnglish
					self.removeProvisionPosTag(law)
					self.addProvisionPosTag(law)
					law.content=law.content.replace("<br>","")
					self.updateArticle(law)
					self.queueDao.updateStatus(law.id,Article.CONTENT_TYPE_LAW,Article.STATUS_WAIT_UPLOAD)

          def findSepcifiedStrInLaw(self,sstr):
                  for row in self.lawDao.getAll():
                          law=self.lawDao.getByOrigin(row.originId,row.providerId,row.isEnglish)  
                          if law and law.content:
                                   if law.content.find(sstr)!=-1:
                                          print law.originId,law.providerId,law.isEnglish
if __name__=="__main__":
        lg=FindLaw()
        lg.findIllegal()
