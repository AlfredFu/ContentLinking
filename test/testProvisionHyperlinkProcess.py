from com.process.ProvisionHyperlinkProcess import *

def testAddProTag():
	phprocess=ProvisionHyperlinkProcess()
	print phprocess.addProvisionPosTag(content4)

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
	
def testMultiPro():
	content="""<a name="i24" re="T"></a>Article 24 After a party legally fulfills its obligation of capital contribution or legally obtains equity through succession, the company fails to issue to it a certificate of capital contribution, record it into the shareholder register or handle registration formalities with the company registration authority in accordance with articles 32,314,56,89   and 33 of the <a href="/law/content.php?content_type=T&origin_id=4685&provider_id=2&isEnglish=Y" class="link_2" re="T" cate="en_href" >Company Law</a>, the said party claims against the company for performance of foregoing obligations, the people's court shall sustain.<a name="end_i24" re="T"></a><br /><br />"""
	
	phprocess=ProvisionHyperlinkProcess()
	
	posList=phprocess.search(content)
	print posList
if __name__=='__main__':
	#print testCheckProvisionExist(testAddProTag(),5)
	#testHyperlinkProvi()
	#testAddRelativeArticleLink()
	testMultiPro()
