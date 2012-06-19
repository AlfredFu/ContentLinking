def testFindAbbrTagPatternStr():
	content="use this card to apply for overdraft in the bank. Zhang's act had violated Paragraph 3, <a href='#' class='link_3'>Article 280</a> (HereinAfter referred to as the Article 280) of <a href='#'>what,tell me why</a> the <a href='/law/content.php?content_type=T&origin_id=470853&provider_id=1&isEnglish=Y' class='link_3' >Criminal Law of the People Republic of China</a> (hereinafter referred to as the ' CriminalL aw ')"
	abbHypePro=AbbreviationHyperlinkProcess()
	matches=abbHypePro.search(content)
	print matches 
	for match in matches:
		content=content[:match[0]]+content[match[1]:]
	#content=content[:matches[0][0]]+content[matches[0][1]:]
	#print content
	
def testPatternContent():
	abbHypePro=AbbreviationHyperlinkProcess()
	content="use this card to apply for overdraft in the bank. Zhang's act had violated Paragraph 3, <a href='#' class='link_3'>Article 280</a> (HereinAfter referred to as the Article 280) of <a href='#'>what,tell me why</a> the <a href='/law/content.php?content_type=T&origin_id=470853&provider_id=1&isEnglish=Y' class='link_3' >Criminal Law of the People Republic of China</a> (hereinafter referred to as the ' Criminal Law '),destiny Criminal Law Article 280 "
	matches=abbHypePro.search(content)
	#print matches
	print content
	for match in matches:
		content=abbHypePro.patternContent(content,match)	
	print content


