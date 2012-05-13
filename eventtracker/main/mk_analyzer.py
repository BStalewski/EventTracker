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
    classes = []

    for link in soup.findAll('a'):
        try:
            print "http://multikino.pl/"+link.get('href')
            gzip_buf = opener.open("http://multikino.pl/"+link.get('href'))
        except:     #fixme - nie czekać na timeout - zrobic lepiej
            continue
        html = StringIO( gzip_buf.read())
        soup2 = bs.BeautifulSoup(html.read())
        for link2 in soup2.findAll('a'):
            try:
                print ( "http://multikino.pl/"+link2.get('href') )
                gzip_buf = opener.open("http://multikino.pl/"+link2.get('href'))
            except:     #fixme - nie czekać na timeout - zrobic lepiej
                print "except -> ", ( "http://multikino.pl/"+link2.get('href') )
                continue

            html = StringIO( gzip_buf.read())
            soup3 = bs.BeautifulSoup(html.read())
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
                        '''
                        elStyles = tmpEl.get('style').split(';')
                        for style in elStyles:
                            if style not in styles:
                                styles.append( style )
                        '''
            for cls in classes:
                newElements = soup3.findAll(True, cls)
                if len( newElements ) > 0:
                    print 'Obiekty klasy:', cls
                for newEl in newElements:
                    print newEl



            for style in styles:
                #newElements = soup3.findAll(style=re.compile(style))
                newElements = soup3.findAll(style=style)
                if len( newElements ) > 0:
                    print 'Obiekty ze stylem:', style
                for newEl in newElements:
                    print newEl
                    '''
                    words = newEl.split(' ')
                    name = newEl[0]
                    surname = newEl[1]
                    print name, surname
                    '''
            #for sibling in soup.find(id="Renny").previous_siblings:
            #   print repr(sibling)
            #print soup3
            #if 'Renny' in soup3.contents.__str__():
            #   print soup3
    
		print 'Znalezione style:', styles
        print 'Znalezione klasy:', classes
        break   #fixme - teraz zatrzymuje się na pierwszym znalezionym żeby było szybciej

#def analyze():
    #return "Something important"

