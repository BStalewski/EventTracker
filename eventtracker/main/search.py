# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



#nie działają polskie znaki
#nie działa jeżeli w nazwie filmu jest obrazek "IMAX"
from models import Obiekt, Url_json
from cStringIO import StringIO
from collections import deque
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

	visited = {}
	link_queue = deque([(rootUrl, 0)])

	addedCount = 0
	jsonPaths = Url_json.objects.filter(url=rootUrl).values()[0]
	paths = json.loads(jsonPaths['json'])

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
		except Exception as e:  #fixme - nie czekać na timeout - zrobic lepiej
			#print "except -> ", highUrl
			continue

		soup = bs.BeautifulSoup(content)
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

		if objectOnSite(soup, paths):
			newObject = Obiekt()
			for (i,path) in enumerate(paths):
				if path == []:
					continue
				else:
					key = 'pole' + str(i+1)
					###value = findFromPath(soup3, path).text
					value = findFromPath(soup, path)
					setattr(newObject, key, value)
					print key, ':',
					try:
						print value
					except:
						pass

			print 'Zapisuje obiekt'
			#raise RuntimeError()
			newObject.save()
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
	el = soup.find(path[0][0])
	pathCopy = path[1:]
	for name, i in pathCopy:
		el = el.contents[i]
		try:
			elName = el.name
		except:
			elName = ''
		if elName != name:
			raise RuntimeError()

	return el
