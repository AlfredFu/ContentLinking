"""
Provide  url parse function for LexisNexis China Online
Since 2012-07-12 
"""

def getUrlParams(linkurl):
	"""
	Get params in url
	Return a dictionary which comprised of param(key is param name ,value is param value)
	Sample:
		if linkurl is '/law/content.php?content_type=T&origin_id=1339854&provider_id=1&isEnglish=Y'
		{'content_type':'T','origin_id':'1339854','provider_id':'1','isEnglish':'Y'} will be returned
	"""
	if linkurl:
		start=linkurl.find('?')+1
		end=linkurl.find('#')
		if start !=-1:
			#paramstr=linkurl[start:] if end==-1 else linkurl[start:end] #since python 2.5
			paramsMap={}
			if end==-1:	
				paramstr=linkurl[start:]
			else:
				paramstr=linkurl[start:end]
			if paramstr:
				params=paramstr.split('&')
				for tmpparam in params:
					tpp=tmpparam.split('=')
					paramsMap[tpp[0]]=tpp[1]	
			return paramsMap

def getUrlAnchor(linkurl):
	"""
	Get anchor in the linkurl
	"""
	if linkurl:
		anchorPos=linkurl.find('#')
		if anchorPos!=-1:
			anchorPos+=1
			return  linkurl[anchorPos:]

def getUrlProvisionNum(linkurl):
	"""
	Get anchor in the linkurl
	"""
	if linkurl:
		anchorPos=linkurl.find('#i')
		if anchorPos!=-1:
			anchorPos+=2
			return  linkurl[anchorPos:]


if __name__=='__main__':
	print getUrlParams('law/content.php?content_type=&origin_id=2222&provider_id=1&isEnglish=Y#i32')
	print getUrlParams('law/content.php?content_type=T&origin_id=2222&provider_id=1&isEnglish=Y')
	print getUrlAnchor('law/content.php?content_type=T&origin_id=2222&provider_id=1&isEnglish=Y#i32')
	print getUrlProvisionNum('law/content.php?content_type=T&origin_id=2222&provider_id=1&isEnglish=Y#i32')
