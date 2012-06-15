import sys
import timeit
import time
sys.path.append('/home/fred/workspace/hyperlink')
from Keyword import *
from DBConnection import *
import threading

class Article:
    keyword=[]
    def __init__(self,row):
        self.id=row['id']
        self.title=row['title']
        self.content=row['content']
        self.dbconn=DBConnection.getConnection('localhost','root','','newlaw')
        self.cursor=self.dbconn.cursor()
    

    def hyperlink(self,keywords):
        print time.asctime()
        repKeywords=[]
        for keyword in keywords:
#if self.content.find(keyword[0]) !=-1:
                self.content=self.content.replace(keyword[0],"<a type='' href=''>"+keyword[0]+"</a>")
        '''
        for keyword in repKeywords:
            self.content=self.content.replace(keyword,"<a type='' href=''>"+keyword+"</a>")
        for keyword in keywords:
            self.content=self.content.replace(keyword[0],"<a type='' href=''>"+keyword[0]+"</a>")
                                              '''
        print time.asctime()

    
    def getAll(self):
        self.cursor.execute("select tax.taxid,tax.title,tax_content.content from tax left join tax_content on tax.taxid=tax_content.taxid where tax.isEnglish='Y' and tax.display=1 and tax.duplicate_flag=0")
        
    def update(self):
        print time.asctime()
        self.cursor.execute("update tax_content set content=%s where taxid=%s",(self.content,self.id))
        self.dbconn.commit()
        print time.asctime()

    def initialHyperlink():
        pass                   

if __name__=='__main__':
    keyword=Keyword()
    keywords=keyword.getAll()
    dbconn=DBConnection.getConnection('localhost','root','','newlaw')
    cursor=dbconn.cursor()
    cursor.execute('use newlaw;')
    cursor.execute("select tax.taxid,tax.title,tax_content.content from tax left join tax_content on tax.taxid=tax_content.taxid where tax.isEnglish='Y' and tax.display=1 and tax.duplicate_flag=0 limit 0,100")
    for row in cursor.fetchall():
        print row[1]
        article=Article({'id':row[0],'title':row[1],'content':row[2]})
        article.hyperlink(keywords)
        if article.content != row[2]:
            article.update()
class Law(Article):
    pass

class Case(Article):
    pass
class CaseSummary(Case):
    pass

