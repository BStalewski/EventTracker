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
rootUrl = 'http://multikino.pl/pl/filmy/'

#def scan_whole_internet():
def analyze(rootUrl):
    opener = urllib2.build_opener()
    opener.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')]
    gzipped = checkGzipped(rootUrl, opener)
    soup = bs.BeautifulSoup(getContent(rootUrl, gzipped, opener))
    styles = []
    classes = []

    for link in soup.findAll('a'):
        try:
            highUrl = constructUrl(rootUrl, link.get('href'))
            content = getContent(highUrl, gzipped, opener)
        except:  #fixme - nie czekać na timeout - zrobic lepiej
            continue
        soup2 = bs.BeautifulSoup(content)
        for link2 in soup2.findAll('a'):
            try:
                lowUrl = constructUrl(highUrl, link2.get('href'))
                print lowUrl
                content = getContent(lowUrl, gzipped, opener)
            except:  #fixme - nie czekać na timeout - zrobic lepiej
                print "except -> ", lowUrl
                continue

            soup3 = bs.BeautifulSoup(content)               

            for person in Person.objects.all():
                foundElements = soup3.findAll(text=re.compile(person.name+" "+person.surname))
                if foundElements != []:
                    print 'Znalezione elementy z nazwiskami:', foundElements
                    for el in foundElements:
                        tmpEl = el.findParent() # nalezy zaczac od rodzica, bo napis nie ma stylu
                        while not tmpEl.get('style') and not tmpEl.get('class'):
                            print "1", tmpEl
                            print '2', tmpEl.get('style')
                            tmpEl = tmpEl.findParent()
                        print 'Rodzic znalezionego elementu:'
                        print tmpEl
                        new_class = tmpEl.get('class')
                        if new_class and new_class not in classes:
                            print 'Dodano nowa klase:', new_class
                            classes.append( new_class )

                        new_style = tmpEl.get('style')
                        if new_style and new_style not in styles:
                            print 'Dodano nowy styl:', new_style
                            styles.append( new_style )


            for cls in classes:
                newElements = soup3.findAll(True, cls)
                if len( newElements ) > 0:
                    print 'Obiekty klasy:', cls
                for newEl in newElements:
                    print newEl

            for style in styles:
                newElements = soup3.findAll(style=style)
                if len( newElements ) > 0:
                    print 'Obiekty ze stylem:', style
                for newEl in newElements:
                    print newEl
    
        print 'Znalezione style:', styles
        print 'Znalezione klasy:', classes
        break   #fixme - teraz zatrzymuje się na pierwszym znalezionym żeby było szybciej

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

