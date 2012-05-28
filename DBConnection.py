import threading
import MySQLdb

class DBConnection:
    instance=None
    mutex=threading.Lock()


    @staticmethod
    def connect(host,username,password='',db='newlaw'):
        DBConnection.instance=MySQLdb.connect(host,username,password,db)
        if DBConnection.instance is None:
            raise Exception('Connect to '+db+' on '+host+' with username:'+username+',password:'+password+' failed')

    @staticmethod
    def getConnection(host,username,password='',db='newlaw'):
        if DBConnection.instance is  None:
            DBConnection.mutex.acquire()
            if DBConnection.instance is None:
                DBConnection.connect(host,username,password,db)
            DBConnection.mutex.release()
        else:
            #log
            pass
        return DBConnection.instance


if __name__=='__main__':
    conn=DBConnection.getConnection('localhost','root','','newlaw')
    if conn:
        cursor=conn.cursor()
        cursor.execute('set names GBK')
        cursor.execute('use lnc')
        cursor.execute('delete from keyword_en')
        conn.commit()
        conn.close()
        conn2=DBConnection.getConnection('localhost','root','','newlaw')
        if conn is conn2:
            print 'conn is conn2'
    else:
        raise Exception("connect to mysql db failed")
