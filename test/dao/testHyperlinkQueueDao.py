#coding=utf-8

from com.dao.HyperlinkQueueDAO import HyperlinkQueueDAO

dao=HyperlinkQueueDAO()

def testCollectStatisticsOfProcessedData():
	for row in dao.collectStatisticsOfProcessedData():
		print row	

if __name__=='__main__':
	testCollectStatisticsOfProcessedData()
