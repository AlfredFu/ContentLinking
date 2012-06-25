import threading
import MySQLdb
from com.util.ConfigOptionUtil import *
from com.util.LogUtil import *

class DBConnUtil:
    instance={}
    mutex=threading.Lock()
    log=getLog()    

    @staticmethod
    def connect(host,username,password='',db='newlaw'):
        return MySQLdb.connect(host,username,password,db)

    @staticmethod
    def getConnection(datasource='db'):
        if datasource not in DBConnUtil.instance or DBConnUtil.instance[datasource] is None:
            dbOption=getConfigSection(datasource)
            DBConnUtil.instance[datasource]=None 
                try:
                        DBConnUtil.mutex.acquire()
                        if DBConnUtil.instance[datasource] is None:
                                DBConnUtil.instance[datasource]=DBConnUtil.connect(dbOption['host'],dbOption['username'],dbOption['password'],dbOption['dbname'])
                    #DBConnUtil.instance[datasource].row_factory=MySQLdb.Row
                        DBConnUtil.mutex.release()
                except Exception,e:
                        DBConnUtil.log.error(e) 
        cursor=DBConnUtil.instance[datasource].cursor()
        cursor.execute("set character_set_client = utf8;")	
        cursor.execute("set character_set_connection = gbk;")	
        cursor.execute("set character_set_results = utf8;")	
        return DBConnUtil.instance[datasource]


if __name__=='__main__':
    conn=DBConnUtil.getConnection()
    if conn:
        cursor=conn.cursor()
        cursor.execute('set names GBK')
        cursor.execute('use lnc')
        cursor.execute('delete from keyword_en')
        conn.commit()
        conn.close()
        conn2=DBConnUtil.getConnection('db')
        if conn is conn2:
        	print 'conn is conn2'
	else:
		print 'conn is not conn2'
        
