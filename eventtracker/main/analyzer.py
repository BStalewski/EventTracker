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

gzip_buf = urllib2.urlopen("http://www.cinema-city.pl/index.php?module=movie&action=repertoire")
buf = StringIO( gzip_buf.read())
html = gzip.GzipFile(fileobj=buf)
soup = bs.BeautifulSoup(html.read())
for link in soup.findAll('a'):
    try:
        gzip_buf = urllib2.urlopen("http://www.cinema-city.pl/"+link.get('href')) #fixme - zafixowane na stałe cinem-city.pl
    except:     #fixme - nie czekać na timeout - zrobic lepiej
        continue
    buf = StringIO( gzip_buf.read())
    html = gzip.GzipFile(fileobj=buf)
    soup2 = bs.BeautifulSoup(html.read())
    for link2 in soup2.findAll('a'):
        try:
            #print "http://www.cinema-city.pl/"+link.get('href')) #fixme - zafixowane na stałe cinem-city.pl
            print ( "http://www.cinema-city.pl/"+link2.get('href') )
            gzip_buf = urllib2.urlopen("http://www.cinema-city.pl/"+link2.get('href')) #fixme - zafixowane na stałe cinem-city.pl
        except:     #fixme - nie czekać na timeout - zrobic lepiej
            print "except -> ", ( "http://www.cinema-city.pl/"+link2.get('href') )
            continue


        buf = StringIO( gzip_buf.read())
        html = gzip.GzipFile(fileobj=buf)
        soup3 = bs.BeautifulSoup(html.read())
        for name in Person

	print soup3.findAll(text=re.compile('Renny'))[0].findParent().findParent()
	#for sibling in soup.find(id="Renny").previous_siblings:
	#	print repr(sibling)
        #print soup3
        if 'Renny' in soup3.contents.__str__():
            print soup3
        
    break   #fixme - teraz zatrzymuje się na pierwszym znalezionym żeby było szybciej

def analyze():
    return "Something important"
