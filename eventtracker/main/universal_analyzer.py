 # -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



#nie działają polskie znaki
#nie działa jeżeli w nazwie filmu jest obrazek "IMAX"
from models import Obiekt, Url_json
from cStringIO import StringIO
from datetime import date, datetime, timedelta
from collections import deque
import BeautifulSoup as bs
import urllib2
import re
import gzip
import sys

import json

keys = 6

#def scan_whole_internet():
def teach(rootUrl, teach_index):
	opener = urllib2.build_opener()
	opener.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')]
	gzipped = checkGzipped(rootUrl, opener)
	styles = []
	classes = []

	visited = {}
	link_queue = deque([(rootUrl, 0)])
	learn_limit = 0
	while True:
		if len(link_queue) == 0:
			print "### PUSTA KOLEJKA LINKOW ###"
			return
		try:
			(highUrl, level) = link_queue.popleft()
			content = getContent(highUrl, gzipped, opener)
			visited[highUrl] = True
		except RuntimeError as e:
			#print e, ':', highUrl
			continue
		except:  #fixme - nie czekać na timeout - zrobic lepiej
			#print "except -> ", highUrl
			continue
		
		soup = bs.BeautifulSoup(content)
		print 'len', len(soup.findAll('a'))
		for link in soup.findAll('a'):
			try:
				lowUrl = constructUrl(highUrl, link.get('href'))
			except RuntimeError as e:
				#print e, ':', link.get('href')
				continue
			except:
				#print "except -> ", highUrl
				continue
			if lowUrl in visited:
				continue
			link_queue.append((lowUrl,level+1))
			visited[lowUrl] = True

		obiekt = Obiekt.objects.all()[teach_index]
		if objectFound(obiekt, soup):
			paths = findPaths(obiekt, soup)
			jsonPaths = json.dumps(paths)
			
			newUrlJson = Url_json(url=rootUrl, json=jsonPaths)
			newUrlJson.save()
			print 'Nauczylem sie na urlu:', highUrl
			return
		learn_limit = learn_limit + 1
		print learn_limit + 1," # ",level," # ",highUrl
		if learn_limit > 123 or level == 2:
			print '### NIE NAUCZYLEM SIE!!! ###:', rootUrl
			return
		
	print 'Nie nauczylem sie na urlu:', rootUrl

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

def getFromPath(soup, path):
	el = soup.find('html')
	path_copy = path[:]
	while path_copy[0][0] != 'html':
		del path_copy[0]
	del path_copy[0] # usuwamy poziom z htmlem, teraz element zerowy jest dzieckiem htmla
	for _, i in path_copy:   # na początku jest obiekt o nazwie documents
		el = el.contents[i]

	return el
	
def notEmptyFields( obj ):
	fields = []
	for i in range(keys):
		key = 'pole' + str(i+1)
		searched = getattr(obj, key)
		if searched == '':
			break
		fields.append(searched)
	return fields

def objectFound( obj, soup ):
	fields = notEmptyFields( obj )
	for field in fields:
		if len( soup.findAll(text=field) )== 0:
			return False
	
	return True
	
def findPaths( obj, soup ):
	paths = []
	for i in range(keys):
		key = 'pole' + str(i+1)
		searched = getattr(obj, key)
		if searched == '':
			paths.append( [] )
		else:
			# fixme: niekoniecznie pierwszy
			# fixme: porządne wyrażenie regularne
			tmpEl = soup.findAll(text=searched)[0].parent
			path_of_tmpEl = []
			while tmpEl is not None:
				place = 0
				sibling = tmpEl.previousSibling 
				while sibling is not None:
					place = place + 1 # uwaga: soup czasami zwraca '\n' jako rodzeństwo
					sibling = sibling.previousSibling
				path_of_tmpEl.append((tmpEl.name,place))
				tmpEl = tmpEl.findParent()
			path_of_tmpEl.reverse()
			while path_of_tmpEl[0][0] != 'html':
				del path_of_tmpEl[0]
			del path_of_tmpEl[0]
			paths.append( path_of_tmpEl )
	print '#### PATHS ####', paths
	return paths
	