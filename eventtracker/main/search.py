# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



#nie działają polskie znaki
#nie działa jeżeli w nazwie filmu jest obrazek "IMAX"
from models import Obiekt, Url_json
from collections import deque
import BeautifulSoup as bs
import urllib2
import re
import sys

import json

from common import *

def search(rootUrl, limit=None):
	opener = urllib2.build_opener()
	opener.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')]
	gzipped = checkGzipped(rootUrl, opener)

	visited = {}
	link_queue = deque([(rootUrl, 0)])

	added = []
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
			continue
		except Exception as e:  #fixme - nie czekać na timeout - zrobic lepiej
			continue

		print highUrl
		soup = bs.BeautifulSoup(content)
		for link in soup.findAll('a'):
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

		if objectOnSite(soup, paths):
			newObject = Obiekt()
			newObject.url = rootUrl
			newObjectCopy = {'url': rootUrl}
			for (i,path) in enumerate(paths):
				if path == []:
					continue
				else:
					key = 'pole' + str(i+1)
					value = findFromPath(soup, path)
					setattr(newObject, key, value)
					newObjectCopy[ key ] = value
					print key, ':',
					try:
						print value
					except:
						pass

			print 'Zapisu obiektu'
			newObject.save()
			added.append(newObjectCopy)
			if limit is not None and len(added) >= limit:
				break
			
	return added

def objectOnSite(soup, paths):
	for (i,path) in enumerate(paths):
		if path != []:
			try:
				findFromPath(soup, path)
			except:
				return False
	return True

def findFromPath(soup, path):
	el = soup
	for name, i in path:
		el = el.contents[i]
		try:
			elName = el.name
		except:
			elName = ''
		if elName != name:
			raise RuntimeError()

	return el

