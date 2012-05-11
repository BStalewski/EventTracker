# -*- coding: UTF-8 -*-

#nie działają polskie znaki
#nie działa jeżeli w nazwie filmu jest obrazek "IMAX"

from cStringIO import StringIO
from datetime import date, datetime, timedelta
import lib.BeautifulSoup as bs
import urllib2
import re
import gzip
import sys

def get_cinema_city(address, place_id, seans_date):
	results = []
	gzip_buf = urllib2.urlopen(address)
	buf = StringIO( gzip_buf.read())
	html = gzip.GzipFile(fileobj=buf)
	soup = bs.BeautifulSoup(html.read())
	movies = soup('table',{'align' : 'center'})[2]('table',{'width' : '483'})[2]('tr')
	i = len(movies) - 1
	while i > 0:
		movie = movies[i]
		movie_id = movie('a')[0].attrs[2][1][6:]
		#wczytywanie opisu filmu (gatunek, reżyseria, czas trwania, opis i inne)
		gzip_buf = urllib2.urlopen('http://www.cinema-city.pl/index.php?module=movie&id='+movie_id)
		buf = StringIO( gzip_buf.read())
		html = gzip.GzipFile(fileobj=buf)
		soup = bs.BeautifulSoup(html.read())
		descriptions = soup('table')[4]('table')[0]('tr')[2]

		opis = gatunek = rezyseria = scenariusz = obsada = rok = produkcja = dlugosc = None
		try:
			for k in range(10): #quick fix
				if descriptions('table')[2]('tr')[k]('td')[0].string == 'Gatunek:' :
					gatunek = descriptions('table')[2]('tr')[k]('em')[0].string
				if descriptions('table')[2]('tr')[k]('td')[0].string == 'Reżyseria:' :
					rezyseria = descriptions('table')[2]('tr')[k]('strong')[0].string
				if descriptions('table')[2]('tr')[k]('td')[0].string == 'Scenariusz:' :
					scenariusz = descriptions('table')[2]('tr')[k]('strong')[0].string
				if descriptions('table')[2]('tr')[k]('td')[0].string == 'Obsada:' :
					obsada = descriptions('table')[2]('tr')[k]('strong')[0].string
				if descriptions('table')[2]('tr')[k]('td')[0].string == 'Rok produkcji:': 
					rok = descriptions('table')[2]('tr')[k]('strong')[0].string
				if descriptions('table')[2]('tr')[k]('td')[0].string == 'Produkcja:' :
					produkcja = descriptions('table')[2]('tr')[k]('strong')[0].string
				if descriptions('table')[2]('tr')[k]('td')[0].string == 'Długość:' :
					dlugosc = descriptions('table')[2]('tr')[k]('strong')[0].string

			#if descriptions('table')[2]('tr')[0]('td')[0].string == 'Gatunek:' :
				#gatunek = descriptions('table')[2]('tr')[0]('em')[0].string
			#if descriptions('table')[2]('tr')[1]('td')[0].string == 'Reżyseria:' :
				#rezyseria = descriptions('table')[2]('tr')[1]('strong')[0].string
			#if descriptions('table')[2]('tr')[2]('td')[0].string == 'Scenariusz:' :
				#scenariusz = descriptions('table')[2]('tr')[2]('strong')[0].string
			#if descriptions('table')[2]('tr')[3]('td')[0].string == 'Obsada:' :
				#obsada = descriptions('table')[2]('tr')[3]('strong')[0].string
			#if descriptions('table')[2]('tr')[4]('td')[0].string == 'Rok produkcji:': 
				#rok = descriptions('table')[2]('tr')[4]('strong')[0].string
			#if descriptions('table')[2]('tr')[5]('td')[0].string == 'Produkcja:' :
				#produkcja = descriptions('table')[2]('tr')[5]('strong')[0].string
			#if descriptions('table')[2]('tr')[6]('td')[0].string == 'Długość:' :
				#dlugosc = descriptions('table')[2]('tr')[6]('strong')[0].string
		except IndexError, e:
			pass
		opis = descriptions('p')[3].string
		#----------------------------------------------------------------------
		title_pl = movie('a', style=re.compile('color:#f5821e'))
		title_ang = movie('h4', style=re.compile('color:#c4c4c4'))
		dates = movie('span', {'class' : 'repgodzinyact'})
		
		j = len(dates) - 1
		while j> -1:
			#print 'Tytuł polski= ',title_pl[0].string # tu się wywaja przy "IMAX"
			#print 'Tytuł oryginalny= ',title_ang[0].string
			#print 'godzina rozpoczecia= ',dates[j].string
			#print 'Gatunek= ',gatunek
			#print 'Rezyseria= ',rezyseria
			#print 'Scenariusz= ',scenariusz
			#print 'Obsada= ',obsada
			#print 'Produkcja= ',produkcja
			#print 'Dlugosc= ',dlugosc
			#print 'Opis= ',opis
			#print '\n'
			
			begin = datetime.combine(seans_date, datetime.strptime(dates[j].string,'%H:%M').time())
			duration = timedelta(minutes = int(dlugosc.strip(' min.')))
			results.append({
					'place'		: place_id,
					'begin'		: begin,
					'end' 		: begin+duration,
					'duration'	: duration,
					'name'		: "Seans " + title_pl[0].string +" (" + title_ang[0].string + ")",
					'description'	: "Gatunek: "+gatunek+", Rezyseria: "+ rezyseria + ", Scenariusz: "+scenariusz+
							  ", Obsada: " + obsada + ", Produkcja:" + produkcja + "cyt(www.cinema-city.pl): "+opis,
					'period'	: None,
					'tag'		: 'cinema city'
			})
			j -=1
			print results[-1]
		i -= 2
	return results

def importer(search_date):
	name_table = eval('{' + open('lib/importer/cinema_config.py', 'r').read() + '}')
	#sys.setdefaultencoding('utf-8')
	for key, value in name_table.items():
		#print "#####WYNIKI DLA: #####",value,"\n\n\n\n\n"
		try:
			wynik = get_cinema_city('http://www.cinema-city.pl/index.php?module=movie&action=repertoire&cid='+
				key+'&dd='+str(search_date.year)+"-"+str(search_date.month)+"-"+str(search_date.day), value, search_date)
		except:
			pass
		else:
			yield wynik