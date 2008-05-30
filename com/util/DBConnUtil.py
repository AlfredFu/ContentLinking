import threading
import MySQLdb
from com.util.ConfigOptionUtil import *
from com.util.LogUtil import *

class DBConnUtil:
    instance=None
    mutex=threading.Lock()
    log=getLog()    

    @staticmethod
    def connect(host,username,password='',db='newlaw'):
        DBConnUtil.instance=MySQLdb.connect(host,username,password,db)
        if DBConnUtil.instance is None:
            raise Exception('Connect to '+db+' on '+host+' with username:'+username+',password:'+password+' failed')

    @staticmethod
    def getConnection():
        dbOption=getConfigSection('db')
        try:
            if DBConnUtil.instance is  None:
                DBConnUtil.mutex.acquire()
                if DBConnUtil.instance is None:
                    DBConnUtil.connect(dbOption['host'],dbOption['username'],dbOption['password'],dbOption['dbname'])
                DBConnUtil.mutex.release()
        except Exception,e:
            DBConnUtil.log.error(e) 
        return DBConnUtil.instance


if __name__=='__main__':
    conn=DBConnUtil.getConnection()
    if conn:
        cursor=conn.cursor()
        cursor.execute('set names GBK')
        cursor.execute('use lnc')
        cursor.execute('delete from keyword_en')
        conn.commit()
        conn.close()
        conn2=DBConnUtil.getConnection()
        if conn is conn2:
            print 'conn is conn2'
        
