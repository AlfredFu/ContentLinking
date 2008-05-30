from com.util.DBConnUtil import *
from com.core.entity.Keyword import *

class KeywordDAO:
    def __init__(self):
        self.conn=DBConnUtil.getConnection()
        self.cursor=self.conn.cursor()
        self.cursor.execute('use lnc')
        self.rep="of the People's Republic of China"


    def getAll(self):
        self.cursor.execute("select keyword,status,type,full_title_keyword_id from keyword_en  limit 0,10")
        for row in self.cursor.fetchall():
            keyword=Keyword()
            keyword.content=row[0]
            keyword.status=row[1]
            keyword.type=row[2]
            keyword.fullTitleKeywordId=row[3]
            yield keyword

    def getById(self,id):
        try:
             self.cursor.execute("select keyword,status,type,full_title_keyword_id from keyword_en where keyword_id=%s" % id)
             row =self.cursor.fetchone()
        except Exception,e:
             #log



        
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
                if self.rep in row[0]:
                    keywordsEn.append((row[0].replace(self.rep,''),'A'))
                row=self.cursor.fetchone()
            self.cursor.execute('use lnc;')
            self.cursor.execute('delete from keyword_en')
            self.conn.commit()
            self.cursor.executemany("insert into keyword_en(keyword,status,type) values(%s,'NOR',%s)",keywordsEn)
            self.conn.commit()
        except Exception,e:
            print "Exception occured:",e        


def testGetAll():
    keywordDAO=KeywordDAO()
    for keyword in keywordDAO.getAll():
        print keyword.content
def testInitialKeyword():
    keywordDAO=KeywordDAO()
    keywordDAO.initialKeyword()
if __name__=='__main__':
#testInitialKeyword() 
    testGetAll()
