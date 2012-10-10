"""
Mail util for hyperlink of LN
"""
import smtplib,email
from email.Message import Message
from com.util.ConfigOptionUtil import *
from com.util.LogUtil import *
#python2.6 and newer use import expression below
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText 
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText 

SMTP_SERVER=getConfigOption('mail','smtp_server')
SMTP_FROM=getConfigOption('mail','smtp_from')
SMTP_USER=getConfigOption('mail','smtp_user')
SMTP_PASSWD=getConfigOption('mail','smtp_passwd')
SMTP_PORT=getConfigOption('mail','smtp_port')

log=getLog()

default_mail_subject="English hyperlink notification"
default_mail_content="""
Hi guys,

Routine English hyperlink process has finished

Best regards
LexisNexis China
"""
def connectToSMTP():
	"""
	Connect to smtp server
	Return a smtp instance which encapsulates a SMTP connection
	"""
	#server=smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
	server=smtplib.SMTP(SMTP_SERVER)
	server.ehlo()
	#server.login(SMTP_USER,SMTP_PASSWD)
	return server

def sendMessage(server,to,subject,content):
	msg=Message()
	msg['Mime-Version']='1.0'
	msg['From']=SMTP_FROM
	msg['To']=to
	msg['Subject']=subject
	msg['Date']=email.Utils.formatdate()
	msg.set_payload(content)
	try:
		failed=server.sendmail(SMTP_USER,to,str(msg))
	except Exception,e:
		#print "send mail to %s failed" % to
		log.error(e)

def sendHtmlMessage(server,to,subject,content):
	"""
	send email with html context
	"""
	msg = MIMEText(content,'html','utf-8')
	msg['Mime-Version']='1.0'
	msg['From']=SMTP_FROM
	msg['To']=to
	msg['Subject'] = subject
	msg['Date']=email.Utils.formatdate()
	try:
		failed=server.sendmail(SMTP_USER,to,str(msg))
			
	except Exception,e:
		log.error(e)
	
	
def sendMail(to,subject=default_mail_subject,content=default_mail_content,isHtml=False):
	if to and subject:
		server=connectToSMTP()
		if isHtml:
			sendHtmlMessage(server,to,subject,content)	
		else:
			sendMessage(server,to,subject,content)	
	
def sendNotification(mailContent='',isHtml=False):
	mailAddrList=['fred.fu@lexisnexis.com']
	#mailAddrList=['13482736200@139.com']
	#mailAddrList=['13482736200@139.com','fred.fu@lexisnexis.com','min.chen@lexisnexis.com','rock.chen@lexisnexis.com','jessica.wang@lexisnexis.com']
	for mail_addr  in mailAddrList:
		sendMail(mail_addr,default_mail_subject,mailContent,isHtml)

if __name__=='__main__':
	sendNotification("Hello Fred")
