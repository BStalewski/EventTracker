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

from common import *

keys = 6

#def scan_whole_internet():
def teach(rootUrl, teach_index):
	opener = urllib2.build_opener()
	opener.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')]
	gzipped = checkGzipped(rootUrl, opener)

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
			print highUrl
			paths = findPaths(obiekt, soup)
			print paths
			jsonPaths = json.dumps(paths)
			
			newUrlJson = Url_json(url=rootUrl, json=jsonPaths)
			newUrlJson.save()
			print 'Nauczylem sie na urlu:', highUrl
			return
		learn_limit = learn_limit + 1
		print learn_limit + 1," # ",level," # ",highUrl
		if learn_limit > 1230 or level == 3:
			print '### NIE NAUCZYLEM SIE!!! ###:', rootUrl
			return
		
	print 'Nie nauczylem sie na urlu:', rootUrl


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
		#if len( soup.findAll(text=re.compile(field)) ) == 0:
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
			#tmpEl = soup.findAll(text=re.comile(searched))[0]
			tmpEl = soup.findAll(text=searched)[0]
			path = []
			while tmpEl is not None:
				place = 0
				sibling = tmpEl.previousSibling 
				while sibling is not None:
					place += 1
					sibling = sibling.previousSibling
				try:
					name = tmpEl.name
				except:
					name = ''
				path.append((name,place))
				tmpEl = tmpEl.parent

			path.reverse()
			del path[0]	#usuwamy pierwszy element [document]
			paths.append( path )
	#print '#### PATHS ####', paths
	return paths
	
