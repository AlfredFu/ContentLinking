from com.process.ManualHyperlinkProcess import *

content="""
<a name="i26" re="T"></a>Article 26 Where the nominal shareholder transfers, pledges or otherwise disposes of the equity registered under its name and the real capital contributor claims such disposition of equity invalid on the ground that it has actual rights to the equity, the people's court may handle the case in accordance with the provisions of <a href="/law/content.php?content_type=T&origin_id=225627&provider_id=1&isEnglish=Y#i106" class="link_2" re="T" cate="manual_en_href" >article 106</a> of the <a href="/law/content.php?content_type=T&origin_id=225627&provider_id=1&isEnglish=Y" class="link_2" re="T" cate="manual_en_href" >Real Rights Law</a> mutatis mutandis.<br />
Where the equity transfer by the nominal shareholder causes losses to the real capital contributor, the real capital contributor claims against the nominal shareholder to bear responsibility of compensation, the people's court shall sustain.<a name="end_i26" re="T"></a><br /><br />
<a name="i27" re="T"></a>Article 27 <a href="/law/content.php?content_type=T&origin_id=225627&provider_id=1&isEnglish=Y#i106" o_href="/law/content.php?content_type=T&origin_id=225627&provider_id=1&isEnglish=Y" class="link_2" re="T" cate="manual_en_href" >article 106</a> of Where any creditor of the company claims against the shareholder registered with the company registration authority, on the ground that such shareholder has not fulfilled its obligation of capital contribution, to bear supplementary compensation liability to the extent of capital not contributed and the interest thereon for the part of debts of the company which the company is unable to repay, and the said shareholder defense on the ground that it is merely an nominal shareholder rather than the real capital contributor, the people's court shall not sustain.<br />
"""
mhp=ManualHyperlinkProcess()

def testSearch():
	print mhp.search(content)

def testPattern():
	pass

testSearch()
	
