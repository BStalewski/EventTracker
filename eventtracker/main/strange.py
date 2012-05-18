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

def objectOnSite(soup, paths):
	for (i,path) in enumerate(paths):
		if path != []:
			try:
				findFromPath(soup, path)
			except:
				return False
	return True

#rootUrl = 'http://multikino.pl/pl/filmy/projekt-x/'
#rootUrl = 'http://multikino.pl/pl/filmy/seksualni-niebezpieczni/'
rootUrl = 'http://multikino.pl/pl/filmy/dyktator/'
opener = urllib2.build_opener()
opener.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')]
gzipped = checkGzipped(rootUrl, opener)
content = getContent(rootUrl, gzipped, opener)

soup = bs.BeautifulSoup(content)

#path = [["body", 3], ["div", 3], ["div", 1], ["div", 1], ["div", 5], ["h1", 1]]
#path = [ [["body", 3], ["div", 3], ["div", 1], ["div", 1], ["div", 11], ["div", 5], ["p", 0]] ]
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

