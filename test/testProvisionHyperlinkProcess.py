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

Article 6 To establish a company, an application for registration shall be filed with the company registration authority.
here the application meets the establishment requirements of this Law, the company registration authority shall register the company as a limited liability company or joint stock limited company. 
Where the application does not meet the establishment requirements of this Law, it shall not be registered as a limited liability company or joint stock limited company.

Article 7 Where any law or administrative regulation provides that the establishment of a company shall be subject to approval, the relevant approval formalities shall be complied with prior to the registration of the company.
The general public may consult the company register at a company registration authority, which shall allow the general public to consult the register.


"""
	content1="""
<pre>
AMENDMENT TO THE CONSTITUTION OF THE PEOPLE'S REPUBLIC OF CHINA<br />
(Adopted at the First Session of  the  Seventh  National  People's<br />
Congress on April 12, 1988  and  promulgated  for  implementation  by  the<br />
Proclamation No. 8 of the National People's Congress on April 12, 1988)<br />
Article 1<br />
Article 11 of the Constitution shall include a new paragraph which reads:<br />
"The state permits the private sector of the economy to exist and  develop<br />
within the limits prescribed by law. The private sector of the economy  is<br />
a complement to the socialist  public  economy.  The  state  protects  the<br />
lawful rights and interests of the private  sector  of  the  economy,  and<br />
exercises guidance, supervision and control over the private sector of the<br />
economy".<br /><br />
Article 2<br />
The fourth paragraph of Article 10 of  the  Constitution,  which  provides<br />
that "no organization or individual may appropriate, buy,  sell  or  lease<br />
land or otherwise engage in the transfer of land by unlawful means", shall<br />
be amended as: "No organization or individual may appropriate,  buy,  sell<br />
or otherwise engage in the transfer of land by unlawful means.  The  right<br />
to the use of land may be transferred according to law".</pre>
<br /><br />
Provided by State Information Center State Legal DatabasesFor Your Reference Only
<br /><br />
 <br />
"""
	content2="""
<br />Circular of the Ministry of Commerce on Enhancing the Administration over Franchise Businesses<br />
<br />March 10, 2005<br />
<br />Competent departments of all provinces, autonomous regions, municipalities directly under the Central Government, municipalities directly under state planning, and Xin Jiang Production and Construction Corps,<br />
<br />Recently, franchising has experienced rapid development in our country as a new mode of circulation and is becoming an effective method for expanding business scale. Reality shows that franchising has served positive purposes in many functions, including increasing consumption, enhancing the development of middle and small businesses, absorbing non-governmental capitals, and boosting employment. But because of a lag in relevant legislation and regulatory administration, a handful of violators have used franchising as a means to cheat in their business and impair the interest of investors. For the purposes of further enhancing the administration over franchising businesses, regulating franchising activities, and promoting a healthy and orderly development of franchising activities, the following notice is issued on relevant activities:<br />
<br />Article 1 Earnestly implementing the Measures for the Administration over Commercial Franchising, and enhancing the level and capability to manage the franchise businesses by law. <br />
The Measures for the Administration over Commercial Franchising (hereafter referred to as the "Measures") is an important regulation on current franchising activities. The Measures set out specific requirements on the qualifications of the franchiser and franchisee, the franchising contract, the information disclosure, advertising and promotion, supervision and management, as well as the procedures that foreign investment companies need to go through and the legal responsibilities they need to take while involved in franchising activities. The promulgation and implementation of the Measures is the basis and guarantee for regulating commercial franchising, protecting the legitimate right and interest of the franchiser and franchisee, facilitating the healthy and orderly development of commercial franchising, and realizing the regularization and legalization of commercial franchising. Commercial administrations at all levels shall enhance their understanding of the Measures, effectively organize the study and training for the Measures, and guarantee the implementation of the Measures. In the meanwhile, administrations at all levels shall localize the regulation in their research for feasible local policies and specific procedures, and raise their level and capability to administer franchising activities by law.<br />
<br />Article 2 Sticking to classified guidance and enhancing the regulatory administration over franchising activities<br />
Franchise is enjoying fast development. It encompasses many industries, and is comparatively difficult to administer. Due to these characteristics, commercial administrations at all levels shall pay attention to the modern circulation development trend and the present situation of the enterprise, stick to the classified guidance principle, and direct the society's franchising activities. Investigation and research shall be strengthened for the development of franchising in special areas and special enterprises in order to get first hand data on these developments. A precaution system shall be established to identify unhealthy trend in time, and to implement dynamic management over those enterprises with illegal activities. Cooperation with the industry and commerce administration, tax administration and public securities administration shall be strengthened so that any enterprises suspected of committing commercial fraud or using franchise as a means to perform chain-selling or disguised chain-selling can be reported to relevant authorities in time. The administrations are also responsible for guiding the enterprises to increase their levels of management, gather development potential, and boost their expanding capacity. <br />
The franchise development situation at different areas and a Franchising Activities Questionnaire for the Year 2004 (see the attachment) shall be sent to the Department of Commercial Reform and Development under the Ministry of Commerce by the end of March 2005.<br />
<br />

"""
	content3="""
<br />Circular of the Ministry of Commerce on Enhancing the Administration over Franchise Businesses<br />
<br />March 10, 2005<br />
<br />Competent departments of all provinces, autonomous regions, municipalities directly under the Central Government, municipalities directly under state planning, and Xin Jiang Production and Construction Corps,<br />
<br />Recently, franchising has experienced rapid development in our country as a new mode of circulation and is becoming an effective method for expanding business scale. Reality shows that franchising has served positive purposes in many functions, including increasing consumption, enhancing the development of middle and small businesses, absorbing non-governmental capitals, and boosting employment. But because of a lag in relevant legislation and regulatory administration, a handful of violators have used franchising as a means to cheat in their business and impair the interest of investors. For the purposes of further enhancing the administration over franchising businesses, regulating franchising activities, and promoting a healthy and orderly development of franchising activities, the following notice is issued on relevant activities:<br />
<br />Article 1 Earnestly implementing the Measures for the Administration over Commercial Franchising, and enhancing the level and capability to manage the franchise businesses by law. <br />
The Measures for the Administration over Commercial Franchising (hereafter referred to as the "Measures") is an important regulation on current franchising activities. The Measures set out specific requirements on the qualifications of the franchiser and franchisee, the franchising contract, the information disclosure, advertising and promotion, supervision and management, as well as the procedures that foreign investment companies need to go through and the legal responsibilities they need to take while involved in franchising activities. The promulgation and implementation of the Measures is the basis and guarantee for regulating commercial franchising, protecting the legitimate right and interest of the franchiser and franchisee, facilitating the healthy and orderly development of commercial franchising, and realizing the regularization and legalization of commercial franchising. Commercial administrations at all levels shall enhance their understanding of the Measures, effectively organize the study and training for the Measures, and guarantee the implementation of the Measures. In the meanwhile, administrations at all levels shall localize the regulation in their research for feasible local policies and specific procedures, and raise their level and capability to administer franchising activities by law.<br />
<br />Article 2 Sticking to classified guidance and enhancing the regulatory administration over franchising activities <br />
Franchise is enjoying fast development. It encompasses many industries, and is comparatively difficult to administer. Due to these characteristics, commercial administrations at all levels shall pay attention to the modern circulation development trend and the present situation of the enterprise, stick to the classified guidance principle, and direct the society's franchising activities. Investigation and research shall be strengthened for the development of franchising in special areas and special enterprises in order to get first hand data on these developments. A precaution system shall be established to identify unhealthy trend in time, and to implement dynamic management over those enterprises with illegal activities. Cooperation with the industry and commerce administration, tax administration and public securities administration shall be strengthened so that any enterprises suspected of committing commercial fraud or using franchise as a means to perform chain-selling or disguised chain-selling can be reported to relevant authorities in time. The administrations are also responsible for guiding the enterprises to increase their levels of management, gather development potential, and boost their expanding capacity. <br />
The franchise development situation at different areas and a Franchising Activities Questionnaire for the Year 2004 (see the attachment) shall be sent to the Department of Commercial Reform and Development under the Ministry of Commerce by the end of March 2005.<br />
<br />Article 3 Regulating expositions of franchise to prevent commercial fraud committed through such expositions <br />
Currently, various expositions act as an effective platform for the promotion of franchise. But some violators use the expositions as a means to commit illegal activities such as fraud and illegal funding. Commercial administrations at all levels shall reinforce their regulatory administration over all kinds of franchise expositions. The organizers of the expositions shall strictly control the qualifications of the franchise exposition attendees to guarantee the legality of the attending enterprises and the authenticity of their promotion activities. Relevant commercial administrations shall reinforce their management over foreign economic and technical expositions related to franchise. Once an enterprise attendee is found of using the exposition to commit commercial fraud, relevant commercial administration shall investigate and prosecute such violators together with the industry and commercial administrations.<br />
<br />Article 4 Increasing publicity to create an environment conducive to the development of franchise<br />
Franchise is still a new form of commerce in our country. Much is unknown about franchise in society. Commercial administrations at all levels shall reinforce the publicity of franchise. They shall use all means to publicize franchises' positive function in promoting the development of middle and small businesses and in increasing employment. This will help the society to better realize the importance of developing and regulating franchise activities. Websites, newspapers, and magazines shall be utilized to produce featured publications on franchising. Emphases of such publications shall be put on introducing the basic knowledge of franchising, foreign franchise legislation and development, and the franchise situation in China; emphases shall also be put on commending franchisees that run their business by law, and exposing the franchisees that operate illegally. By combining special and general promotions of franchising, the franchisees will be more conscious of the legality of their operation, and a healthy social environment conducive to the development of franchise will be produced.<br />
<br />Article 5 Fully utilizing franchise industry associations and enhancing self-discipline in the industry <br />
Together with the transformation of the functions of the government, commercial administrations at all levels shall fully utilize the functions of franchise associations as the bridge and link between the government and the franchisees. Commercial administrations at all levels shall promote education and training in this regard, and se up examples of commercial credit to emphasize the concept and consciousness of it, and to gradually establish a credit evaluation system for the franchising industry. They shall reinforce training in the franchise industry by utilizing all forms and means to train the personnel in the franchise industry, and to guide the franchisees to realize standardized and scientific management of their enterprises in order to enhance their core competition capabilities. Relevant laws and regulations shall be obeyed to create regulations, restrictions, and moral standard for the franchising industry. The functions of industry associations to coordinate, serve, and supervise shall be fully utilized to increase self-discipline in the industry, and to promote healthy development of the franchising industry.<br />
<br />Attachment: Franchising Activities Questionnaire<br />
"""
	content4="""
<br />Circular of the Ministry of Commerce on Enhancing the Administration over Franchise Businesses<br />
<br />March 10, 2005<br />
<br />Competent departments of all provinces, autonomous regions, municipalities directly under the Central Government, municipalities directly under state planning, and Xin Jiang Production and Construction Corps,<br />
<br />Recently, franchising has experienced rapid development in our country as a new mode of circulation and is becoming an effective method for expanding business scale. Reality shows that franchising has served positive purposes in many functions, including increasing consumption, enhancing the development of middle and small businesses, absorbing non-governmental capitals, and boosting employment. But because of a lag in relevant legislation and regulatory administration, a handful of violators have used franchising as a means to cheat in their business and impair the interest of investors. For the purposes of further enhancing the administration over franchising businesses, regulating franchising activities, and promoting a healthy and orderly development of franchising activities, the following notice is issued on relevant activities:<br />
<br />Article 1 Earnestly implementing the Measures for the Administration over Commercial Franchising, and enhancing the level and capability to manage the franchise businesses by law. <br />
The Measures for the Administration over Commercial Franchising (hereafter referred to as the "Measures") is an important regulation on current franchising activities. The Measures set out specific requirements on the qualifications of the franchiser and franchisee, the franchising contract, the information disclosure, advertising and promotion, supervision and management, as well as the procedures that foreign investment companies need to go through and the legal responsibilities they need to take while involved in franchising activities. The promulgation and implementation of the Measures is the basis and guarantee for regulating commercial franchising, protecting the legitimate right and interest of the franchiser and franchisee, facilitating the healthy and orderly development of commercial franchising, and realizing the regularization and legalization of commercial franchising. Commercial administrations at all levels shall enhance their understanding of the Measures, effectively organize the study and training for the Measures, and guarantee the implementation of the Measures. In the meanwhile, administrations at all levels shall localize the regulation in their research for feasible local policies and specific procedures, and raise their level and capability to administer franchising activities by law.<br />
<br />Article 2 Sticking to classified guidance and enhancing the regulatory administration over franchising activities <br />
Franchise is enjoying fast development. It encompasses many industries, and is comparatively difficult to administer. Due to these characteristics, commercial administrations at all levels shall pay attention to the modern circulation development trend and the present situation of the enterprise, stick to the classified guidance principle, and direct the society's franchising activities. Investigation and research shall be strengthened for the development of franchising in special areas and special enterprises in order to get first hand data on these developments. A precaution system shall be established to identify unhealthy trend in time, and to implement dynamic management over those enterprises with illegal activities. Cooperation with the industry and commerce administration, tax administration and public securities administration shall be strengthened so that any enterprises suspected of committing commercial fraud or using franchise as a means to perform chain-selling or disguised chain-selling can be reported to relevant authorities in time. The administrations are also responsible for guiding the enterprises to increase their levels of management, gather development potential, and boost their expanding capacity. <br />
The franchise development situation at different areas and a Franchising Activities Questionnaire for the Year 2004 (see the attachment) shall be sent to the Department of Commercial Reform and Development under the Ministry of Commerce by the end of March 2005.<br />
<br />Article 3 Regulating expositions of franchise to prevent commercial fraud committed through such expositions <br />
Currently, various expositions act as an effective platform for the promotion of franchise. But some violators use the expositions as a means to commit illegal activities such as fraud and illegal funding. Commercial administrations at all levels shall reinforce their regulatory administration over all kinds of franchise expositions. The organizers of the expositions shall strictly control the qualifications of the franchise exposition attendees to guarantee the legality of the attending enterprises and the authenticity of their promotion activities. Relevant commercial administrations shall reinforce their management over foreign economic and technical expositions related to franchise. Once an enterprise attendee is found of using the exposition to commit commercial fraud, relevant commercial administration shall investigate and prosecute such violators together with the industry and commercial administrations.<br />
<br />Article 4 Increasing publicity to create an environment conducive to the development of franchise<br />
Franchise is still a new form of commerce in our country. Much is unknown about franchise in society. Commercial administrations at all levels shall reinforce the publicity of franchise. They shall use all means to publicize franchises' positive function in promoting the development of middle and small businesses and in increasing employment. This will help the society to better realize the importance of developing and regulating franchise activities. Websites, newspapers, and magazines shall be utilized to produce featured publications on franchising. Emphases of such publications shall be put on introducing the basic knowledge of franchising, foreign franchise legislation and development, and the franchise situation in China; emphases shall also be put on commending franchisees that run their business by law, and exposing the franchisees that operate illegally. By combining special and general promotions of franchising, the franchisees will be more conscious of the legality of their operation, and a healthy social environment conducive to the development of franchise will be produced.<br />
<br />Article 5 Fully utilizing franchise industry associations and enhancing self-discipline in the industry <br />
Together with the transformation of the functions of the government, commercial administrations at all levels shall fully utilize the functions of franchise associations as the bridge and link between the government and the franchisees. Commercial administrations at all levels shall promote education and training in this regard, and se up examples of commercial credit to emphasize the concept and consciousness of it, and to gradually establish a credit evaluation system for the franchising industry. They shall reinforce training in the franchise industry by utilizing all forms and means to train the personnel in the franchise industry, and to guide the franchisees to realize standardized and scientific management of their enterprises in order to enhance their core competition capabilities. Relevant laws and regulations shall be obeyed to create regulations, restrictions, and moral standard for the franchising industry. The functions of industry associations to coordinate, serve, and supervise shall be fully utilized to increase self-discipline in the industry, and to promote healthy development of the franchising industry.<br />
<br />Attachment: Franchising Activities Questionnaire<br />
"""
	#print  phprocess.addProvisionPosTag(content1)
	#print  phprocess.addProvisionPosTag(content2)
	#print phprocess.addProvisionPosTag(content)
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
	
if __name__=='__main__':
	print testAddProTag()
	#print testCheckProvisionExist(testAddProTag(),5)
	#testHyperlinkProvi()
	#testAddRelativeArticleLink()
