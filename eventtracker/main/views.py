# Create your views here.

from django.http import HttpResponse
import analyzer
import mk_analyzer
import universal_analyzer as ua

def main( request, url='http://multikino.pl/pl/filmy/' ):
    #content = mk_analyzer.analyze()
    content = ua.analyze(url)
    return HttpResponse(content)

def multikino( request ):
    return main(request, url='http://multikino.pl/pl/filmy/')

def cinemacity( request ):
    return main(request, url='http://www.cinema-city.pl/index.php?module=movie&action=repertoire')

