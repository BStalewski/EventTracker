 # -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



#nie działają polskie znaki
#nie działa jeżeli w nazwie filmu jest obrazek "IMAX"
from models import Obiekt, Url_json
from cStringIO import StringIO
from datetime import date, datetime, timedelta
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
	soup = bs.BeautifulSoup(getContent(rootUrl, gzipped, opener))
	styles = []
	classes = []

	visited = {}
	visited[rootUrl] = True
	for link in soup.findAll('a'):
		try:
			highUrl = constructUrl(rootUrl, link.get('href'))
			if highUrl in visited:
				continue
			content = getContent(highUrl, gzipped, opener)
			visited[highUrl] = True
		except:  #fixme - nie czekać na timeout - zrobic lepiej
			continue
		soup2 = bs.BeautifulSoup(content)
		for link2 in soup2.findAll('a'):
			# jeżeli tekst w linku jest pusty to to nie jest odnośnik filmu ----------
			if len(link2.text) == 0 :
				continue
			try:
				lowUrl = constructUrl(highUrl, link2.get('href'))
				print lowUrl
				if lowUrl in visited:
					continue
				content = getContent(lowUrl, gzipped, opener)
				visited[lowUrl] = True
			except RuntimeError as e:
				print e, ':', link2.get('href')
			except:  #fixme - nie czekać na timeout - zrobic lepiej
				print "except -> ", lowUrl
				continue

			soup3 = bs.BeautifulSoup(content)			   
			obiekt = Obiekt.objects.all()[teach_index]
			if not objectFound(obiekt, soup3):
				continue
			
			paths = findPaths(obiekt, soup3)
			jsonPaths = json.dumps(paths)
			
			newUrlJson = Url_json(url=rootUrl, json=jsonPaths)
			newUrlJson.save()
			print 'Nauczylem sie na urlu:', rootUrl
			return
		break
	print 'Nie nauczylem sie na urlu:', rootUrl

def getDomain(url):
	domainEnd = url.find('/', 7) if url[:4] == 'http' else url.find('/')
	potentialDomain = url[:domainEnd] if domainEnd != -1 else url
	return potentialDomain if potentialDomain.count('.') > 0 else None

def constructUrl(baseUrl, ahrefUrl):
	ahrefDomain = getDomain( ahrefUrl)
	baseDomain = getDomain( baseUrl )
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
		print len( soup.findAll(text=field) )
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
	