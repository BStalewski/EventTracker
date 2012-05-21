 # -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#nie działają polskie znaki
#nie działa jeżeli w nazwie filmu jest obrazek "IMAX"
from models import Obiekt, Url_json
from datetime import date, datetime, timedelta
from collections import deque
import BeautifulSoup as bs
import urllib2
import re
import sys

import json

from common import *

keys = 6
limit = 1000

def teach(rootUrl, key1, key2=''):
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
			continue
		except:  #fixme - nie czekać na timeout - zrobic lepiej
			continue
		
		soup = bs.BeautifulSoup(content)
		print highUrl
		for link in soup.findAll('a'):
			print link.get('href')
			try:
				lowUrl = constructUrl(highUrl, link.get('href'))
			except RuntimeError as e:
				continue
			except:
				continue
			if lowUrl in visited:
				continue
			link_queue.append((lowUrl,level+1))
			visited[lowUrl] = True

		obiekt = Obiekt.objects.filter(url=rootUrl, pole1=key1, pole2=key2)[0]
		if objectFound(obiekt, soup):
			print highUrl
			paths = findPaths(obiekt, soup)
			print paths
			jsonPaths = json.dumps(paths)
			
			newUrlJson = Url_json(url=rootUrl, json=jsonPaths)
			newUrlJson.save()
			print 'Nauczylem sie na urlu:', highUrl
			return (paths, highUrl)

		learn_limit = learn_limit + 1
		print learn_limit + 1," # ",level," # ",highUrl
		if learn_limit > limit or level == 3:
			print '### Nie nauczylem sie ###:', rootUrl
			return
		
	print 'Nie nauczylem sie na urlu:', rootUrl

def notEmptyFields( obj ):
	fields = []
	for i in range(keys):
		key = 'pole' + str(i+1)
		searched = getattr(obj, key)
		if searched == '':
			break
		fields.append(searched)
	return fields

#regular = '[\s\/]*'
regular = '\s*'

def objectFound( obj, soup ):
	fields = notEmptyFields( obj )
	for field in fields:
		regexp = regular + field + regular
		#if len( soup.findAll(text=re.compile(field)) ) == 0:
		#if len( soup.findAll(text=regular) ) == 0:
		if len( soup.findAll(text=re.compile(regexp)) )== 0:
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
			regexp = regular + searched + regular
			tmpEl = soup.findAll(text=re.compile(regexp))[0]
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
	return paths
	
