from cStringIO import StringIO
import gzip

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
