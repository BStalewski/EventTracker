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
def search(rootUrl):
	opener = urllib2.build_opener()
	opener.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')]
	gzipped = checkGzipped(rootUrl, opener)
	soup = bs.BeautifulSoup(getContent(rootUrl, gzipped, opener))

	visited = {}
	visited[rootUrl] = True
	addedCount = 0
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

			jsonPaths = Url_json.objects.filter(url=rootUrl).values()[0]
			paths = json.loads(jsonPaths['json'])
			soup3 = bs.BeautifulSoup(content)
			
			if lowUrl == 'http://multikino.pl/pl/filmy/dyktator/':
				print paths
				for path in paths:
					if path != []:
						for x in findFromPath(soup3, path).contents:
							print x
				print 'qweqeweerewrerwr'

			if objectOnSite(soup3, paths):
				newObject = Obiekt()
				for (i,path) in enumerate(paths):
					if path == []:
						continue
					else:
						key = 'pole' + str(i+1)
						value = findFromPath(soup3, path).text
						setattr( newObject, key, value )
						print key, ':', value

				print paths
				print 'WOW, wywalam sie a potem zapisuje obiekt:)'
				print lowUrl
				print newObject
				#raise RuntimeError()
				#newObject.save()
				addedCount += 1
			
	return addedCount

def objectOnSite(soup, paths):
	for (i,path) in enumerate(paths):
		if path != []:
			try:
				findFromPath(soup, path)
			except:
				return False
	return True

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

def findFromPath(soup, path):
	el = soup.find('html')
	for name, i in path:
		el = el.contents[i]
		if el.name != name:
			raise RuntimeError()

	return el
	
