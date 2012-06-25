from com.process.ProvisionHyperlinkProcess import *

def testAddProTag():
	phprocess=ProvisionHyperlinkProcess()
	content="""
Chapter I General Provisions
Article 1 This Law is enacted for the purposes of regulating the organization and operation of companies, protecting the legitimate rights and interests of companies, shareholders and creditors, maintaining the socialist economic order, and promoting the development of the socialist market economy

Article 2 The term company as referred to in this Law means a limited liability company or a joint stock company limited established within the territory of the Peoples Republic of China in accordance with the provisions of this law

Article 3 A company is an enterprise legal person, which has independent legal person property and enjoys the right to legal person property. It shall bear liability for its debts with all its assets. For a limited liability company, a shareholder shall be liable for the company to the extent of the capital contributions it has paid. For a joint stock limited company, a shareholder shall be liable for the company to the extent of the shares it has subscribed to.

Article 4 The shareholders of a company shall be entitled to enjoy a return on capital, participate in making important decisions, appoint managers and enjoy other shareholder rights.

Article 5 In conducting its business operations, a company shall comply with laws and administrative regulations, social standards, and business standards. It shall act in good faith, accept the supervision of the government and general public, and act in a socially responsible way.
The legitimate rights and interests of a company shall be protected by law and may not be trespassed against.

Article 6 To establish a company, an application for registration shall be filed with the company registration authority. Where the application meets the establishment requirements of this Law, the company registration authority shall register the company as a limited liability company or joint stock limited company. Where the application does not meet the establishment requirements of this Law, it shall not be registered as a limited liability company or joint stock limited company.
Article 7 Where any law or administrative regulation provides that the establishment of a company shall be subject to approval, the relevant approval formalities shall be complied with prior to the registration of the company.
The general public may consult the company register at a company registration authority, which shall allow the general public to consult the register.

"""
	return phprocess.addProvisionPosTag(content)

def testCheckProvisionExist(content,itemId):
	phprocess=ProvisionHyperlinkProcess()
	return phprocess.checkProvisionExist(content,itemId)	
	
	
def testHyperlinkProvi():
	keywordProcess=ProvisionHyperlinkProcess()
	#keywordProcess.process()
	i=1
	for queueItem in keywordProcess.queueDao.getAll():
		if i>1:break
		i+=1
		article=keywordProcess.getArticle(queueItem)	
		#keywordProcess.updateOprLoadStatus(queueItem)
		#article.content=keywordProcess.eraseHyperlink(article.content)
		#posTupleList=keywordProcess.search(article.content)
		#article=keywordProcess.pattern(article,posTupleList)
		#print posTupleList
		print article.content
		#print article.content
		keywordProcess.process(article)
		keywordProcess.updateArticle(article)

def testAddRelativeArticleLink():
	phprocess=ProvisionHyperlinkProcess()
	for queueItem in phprocess.queueDao.getByContentTypeStatus('T','9'):
		article=phprocess.getArticle(queueItem)
		if article:
			article.content=phprocess.removeProvisionRelativeArticleLink(article.content)
			phprocess.addProvisionRelativeArticleLink(article)
	
if __name__=='__main__':
	#print testAddProTag()
	#print testCheckProvisionExist(testAddProTag(),5)
	#testHyperlinkProvi()
	testAddRelativeArticleLink()
