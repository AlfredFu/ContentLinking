import threading
import MySQLdb
from com.util.ConfigOptionUtil import *
from com.util.LogUtil import *

def escapeString(str):
	if str:
		return MySQLdb.escape_string(str)

class DBConnUtil:
    instance={}
    mutex=threading.Lock()
    log=getLog()    

    @staticmethod
    def connect(host,username,password='',db='newlaw'):
	"""
	Connect to database server host in 'host' with username password
	"""
        return MySQLdb.connect(host,username,password,db)

    @staticmethod
    def getConnection(datasource='db'):
        if datasource not in DBConnUtil.instance or DBConnUtil.instance[datasource] is None:
            dbOption=getConfigSection(datasource)#get meta description of database
            DBConnUtil.instance[datasource]=None 
            try:
            	DBConnUtil.mutex.acquire()
            	if DBConnUtil.instance[datasource] is None:
            		DBConnUtil.instance[datasource]=DBConnUtil.connect(dbOption['host'],dbOption['username'],dbOption['password'],dbOption['dbname'])
                    	#DBConnUtil.instance[datasource].row_factory=MySQLdb.Row
                        DBConnUtil.mutex.release()
        		cursor=DBConnUtil.instance[datasource].cursor()
        		cursor.execute("set character_set_client = utf8;")	
       			cursor.execute("set character_set_connection = gbk;")	
        		cursor.execute("set character_set_results = utf8;")	
			cursor.execute("set wait_timeout=3600;")
            except Exception,e:
                DBConnUtil.log.error(e) 
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
        
