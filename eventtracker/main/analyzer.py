# -*- coding: UTF-8 -*-

#nie działają polskie znaki
#nie działa jeżeli w nazwie filmu jest obrazek "IMAX"
from models import Person
from cStringIO import StringIO
from datetime import date, datetime, timedelta
import BeautifulSoup as bs
import urllib2
import re
import gzip
import sys

#start = "index.php?module=movie&action=repertoire"
#domena = "http://www.cinema-city.pl/"

start = "/pl/filmy/"
domena = "http://multikino.pl"

#def scan_whole_internet():
def analyze():
	gzipped = True
	opener = urllib2.build_opener()
	opener.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')]
	gzip_buf = opener.open(domena+start)
	#gzip_buf = urllib2.urlopen("http://www.cinema-city.pl/index.php?module=movie&action=repertoire")
	buf = StringIO( gzip_buf.read())
	html = gzip.GzipFile(fileobj=buf)
	try:
		soup = bs.BeautifulSoup(html.read())
	except:
		print "multimulit"
		gzipped = False
		gzip_buf = opener.open(domena+start)
		buf = StringIO( gzip_buf.read())
		soup = bs.BeautifulSoup(buf.read())
	styles = []

	for link in soup.findAll('a'):
		try:
			gzip_buf = opener.open(domena+link.get('href')) #fixme - zafixowane na stałe cinem-city.pl
		except:	 #fixme - nie czekać na timeout - zrobic lepiej
			continue
		buf = StringIO( gzip_buf.read())
		if(gzipped):
			html = gzip.GzipFile(fileobj=buf)
			soup2 = bs.BeautifulSoup(html.read())
		else:
			soup2 = bs.BeautifulSoup(buf.read())			
		for link2 in soup2.findAll('a'):
			try:
				#print "http://www.cinema-city.pl/"+link.get('href')) #fixme - zafixowane na stałe cinem-city.pl
				print ( domena+link2.get('href') )
				gzip_buf = opener.open(domena+link2.get('href')) #fixme - zafixowane na stałe cinem-city.pl
			except:	 #fixme - nie czekać na timeout - zrobic lepiej
				print "except -> ", ( domena+link2.get('href') )
				continue

			buf = StringIO( gzip_buf.read())
			if(gzipped):
				html = gzip.GzipFile(fileobj=buf)
				soup3 = bs.BeautifulSoup(html.read())
			else:
				soup3 = bs.BeautifulSoup(buf.read())				
			for person in Person.objects.all():
				try:
					foundElements = soup3.findAll(text=re.compile(person.name+" "+person.surname))
					if foundElements != []:
						print foundElements
						for el in foundElements:
							print 'AAAAA'
							tmpEl = el.findParent() # nalezy zaczac od rodzica, bo napis nie ma stylu
							while not tmpEl.get('style'):
								print "1", tmpEl
								print '2', tmpEl.get('style')
								tmpEl = tmpEl.findParent()
							print tmpEl
							if tmpEl.get('style') not in styles:
								styles.append( tmpEl.get('style') )
							'''
							elStyles = tmpEl.get('style').split(';')
							for style in elStyles:
								if style not in styles:
									styles.append( style )
							'''

					for style in styles:
						print style
						#newElements = soup3.findAll(style=re.compile(style))
						newElements = soup3.findAll(style=style)
						print 'TADAAAM'
						print newElements
						for newEl in newElements:
							print newEl.findParent()
							'''
							words = newEl.split(' ')
							name = newEl[0]
							surname = newEl[1]
							print name, surname
							'''

				except:
					continue
			#for sibling in soup.find(id="Renny").previous_siblings:
			#   print repr(sibling)
			#print soup3
			#if 'Renny' in soup3.contents.__str__():
			#   print soup3
	
		print "STYLEZ:", styles
		break   #fixme - teraz zatrzymuje się na pierwszym znalezionym żeby było szybciej

#def analyze():
	#return "Something important"
