#!/usr/bin/env python
# coding=utf-8
import sys
sys.path.append("/home/fred/workspace/EnglishHyperlink")
from com.process import *

class FindLaw(HyperlinkProcess):
        def __init__(self):
                super(FindLaw,self).__init__()  
                self.illegalProvisionPosTagPattern=re.compile(r'<a re="T" name="(end_)?i[\d\.]+"></a>')

        def findIllegal(self):
                for row in self.lawDao.getAll():
                        law=self.lawDao.getByOrigin(row.originId,row.providerId,row.isEnglish)  
                        if law and law.content:
                                 if self.illegalProvisionPosTagPattern.search(law.content):
                                        print law.originId,law.providerId,law.isEnglish 

if __name__=="__main__":
        lg=FindLaw()
        lg.findIllegal()
