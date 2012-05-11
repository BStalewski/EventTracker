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

#def scan_whole_internet():
def analyze():
    opener = urllib2.build_opener()
    opener.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')]
    gzip_buf = opener.open("http://multikino.pl/pl/filmy/")
    html = StringIO( gzip_buf.read())
    #soup = bs.BeautifulSoup(html.read())
    soup = bs.BeautifulSoup(html.read())
    styles = []

    for link in soup.findAll('a'):
        try:
            gzip_buf = opener.open("http://multikino.pl/pl/filmy/"+link.get('href'))
        except:     #fixme - nie czekać na timeout - zrobic lepiej
            continue
        html = StringIO( gzip_buf.read())
        soup2 = bs.BeautifulSoup(html.read())
        for link2 in soup2.findAll('a'):
            try:
                print ( "http://multikino.pl/pl/filmy/"+link2.get('href') )
                gzip_buf = opener.open("http://multikino.pl/pl/filmy/"+link2.get('href'))
            except:     #fixme - nie czekać na timeout - zrobic lepiej
                print "except -> ", ( "http://multikino.pl/pl/filmy/"+link2.get('href') )
                continue

            html = StringIO( gzip_buf.read())
            soup3 = bs.BeautifulSoup(html.read())
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

