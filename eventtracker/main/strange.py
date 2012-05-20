from BeautifulSoup import BeautifulSoup
import re

doc = '''<html><head><title style="color: blue;" class="cls">Page title</title></head>
	   <body><p id="firstpara" align="center">This is paragraph <b>one</b></p>
	   <p id="secondpara" align="blah">This is paragraph <b>two</b></p>
	   </html>'''
'''
soup = BeautifulSoup(doc)

print soup.contents[0].contents[0].contents[0].get('class')
print soup.contents[0].contents[0].get('class')
print soup.findAll(style='color: blue;')
print soup.findAll(True, 'cls')

ps = soup.findAll('p')
print '-------'
print ps[0]
print ps[0].nextSibling

print soup
'''

from cStringIO import StringIO
from datetime import date, datetime, timedelta
import BeautifulSoup as bs
import urllib2
import re
import gzip
import sys

import json

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

def findFromPathNew(soup, path):
	el = soup.find(path[0][0])
	pathCopy = path[1:]
	for name, i in pathCopy:
		el = el.contents[i]
		try:
			elName = el.name
		except:
			elName = ''
		print elName, i
		if elName != name:
			raise RuntimeError()

	return el

def objectOnSite(soup, paths):
	for (i,path) in enumerate(paths):
		if path != []:
			try:
				findFromPath(soup, path)
			except:
				return False
	return True

def objectFound( obj, soup ):
	fields = notEmptyFields( obj )
	for field in fields:
		print 'try:', field
		#if len( soup.findAll(text=field) )== 0:
		if len( soup.findAll(text=re.compile(field)) ) == 0:
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
	print '#### PATHS ####', paths
	return paths
	
keys = 6
def notEmptyFields( obj ):
	fields = []
	for i in range(keys):
		key = 'pole' + str(i+1)
		searched = getattr(obj, key)
		if searched == '':
			break
		fields.append(searched)
	return fields


#rootUrl = 'http://multikino.pl/pl/filmy/projekt-x/'
#rootUrl = 'http://multikino.pl/pl/filmy/seksualni-niebezpieczni/'
#rootUrl = 'http://multikino.pl/pl/filmy/dyktator/'
rootUrl = 'http://multikino.pl/pl/filmy/avengers-3d-dubbing/'
opener = urllib2.build_opener()
opener.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')]
gzipped = checkGzipped(rootUrl, opener)
content = getContent(rootUrl, gzipped, opener)

soup = bs.BeautifulSoup(content)
'''
paths = [
	[["body", 3], ["div", 3], ["div", 1], ["div", 1], ["div", 5], ["h1", 1]],
	[["body", 3], ["div", 3], ["div", 1], ["div", 1], ["div", 11], ["div", 5], ["p", 0]],
	[],
	[],
	[],
	[]
]

print objectOnSite(soup, paths)

for path in paths:
	if path != []:
		for x in findFromPath(soup, path).contents:
			print x
'''
class x:
	pole1 = 'Avengers 3D - dubbing'
	pole2 = 'Joss Whedon'
	pole3 = ''
	pole4 = ''
	pole5 = ''
	pole6 = ''

ooo = x()

#print objectFound(ooo, soup)
paths = findPaths(ooo, soup)
x1 = findFromPathNew(soup, paths[0])
x2 = findFromPathNew(soup, paths[1])

print x1
print x2
