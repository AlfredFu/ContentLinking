import sys
sys.path.append('/home/fred/workspace/hyperlink')
from DBConnection import *


class Keyword:
    keyword=''
    status='NOR'
    type='F'
    fullTitleKeywordId=None
    dbconn=None
    cursor=None
        
    def __init__(self):
# self.dbconn=DBConnection.getConnection(self.host,self.username,self.password,self.db)
        self.dbconn=DBConnection.getConnection('localhost','root','','newlaw')
        self.cursor=self.dbconn.cursor()
        self.rep="of the People's Republic of China"

    def deleteById(self,id):
        if id:
            self.cursor.execute('delete from keyword_en where id=%s',id)
            self.dbconn.commit()

    def getKeywordByFullTitleKeywordId(self,id):
        if id:
            self.cursor.execute('select keyword_id as id,keyword,status,type,full_title_keyword_id from keyword_en where full_title_keyword_id=%s',id)
            row=self.cursor.fetchone()
            if row:
               self.id=row[0]
               self.keyword=row[1]
               self.status=row[2]
               self.type=row[3] 

    def insert(self):
        pass
    def getAll(self):
        self.cursor.execute('use lnc')
        self.cursor.execute("select keyword,status,type,full_title_keyword_id from keyword_en where status='NOR' limit 0,10000")
        return self.cursor.fetchall()

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
#print row
                row=self.cursor.fetchone()
            self.cursor.execute('use lnc;')
            self.cursor.execute('delete from keyword_en')
            self.dbconn.commit()
            print len(keywordsEn)
            for times in range(23):
                self.cursor.executemany("insert into keyword_en(keyword,status,type) values(%s,'NOR',%s)",keywordsEn)
            self.dbconn.commit()
        except Exception,e:
            print "Exception occured:",e        

            
if __name__=='__main__':
    keyword=Keyword()
#keyword.initialKeyword()
    print "keyword num:",len(keyword.getAll())
