# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
from cStringIO import StringIO
import gzip

def readSource(name):
    '''Reads content from a file/url passed in the argument.'''
    if name.startswith('http://') or name.startswith('www'):
        opener = urllib2.build_opener()
        opener.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')]
        gzipped = checkGzipped(name, opener)
        return getContent(name, gzipped, opener)
    else:
        with open(name, 'rb') as f:
            content = f.read()
        return content

def getDomain(url):
	domainEnd = url.find('/', 7) if url[:4] == 'http' else url.find('/')
	potentialDomain = url[:domainEnd] if domainEnd != -1 else url
	return potentialDomain if potentialDomain.count('.') > 0 else None

def constructUrl(baseUrl, ahrefUrl):
	ahrefDomain = getDomain( ahrefUrl)
	baseDomain = getDomain( baseUrl )
	if ahrefUrl.startswith('index.php'):	#fixme - qiuck fix do cinema city
		return baseDomain + "/"+ahrefUrl
	if ahrefDomain:
		if baseDomain != ahrefDomain:
			raise RuntimeError("External domain")
		return ahrefUrl
	else:
		return baseDomain + ahrefUrl if ahrefUrl[0] == '/' else baseUrl + ahrefUrl

def checkGzipped(url, opener):
	gzip_buf = opener.open(url)
	buf = StringIO(gzip_buf.read())
	html = gzip.GzipFile(fileobj=buf)
	try:
		html.read()
	except:
		return False
	else:
		return True
			
def getContent(url, gzipped, opener):
	gzip_buf = opener.open(url)
	buf = StringIO(gzip_buf.read())
	if gzipped:
		html = gzip.GzipFile(fileobj=buf)
		return html.read()
	else:
		return buf.read()

