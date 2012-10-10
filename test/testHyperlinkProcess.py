#coding=utf-8 
from com.process import *
from com.util.lexismail import *

if __name__=="__main__":
	hp=HyperlinkProcess()
	mailcontent= hp.collectStatistics()
	sendNotification(mailcontent,True)	
