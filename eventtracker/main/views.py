# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

import universal_analyzer as ua
from search import search
from forms import FirstForm

def main( request, url='http://multikino.pl/pl/filmy/'):
    content = ua.teach(url,0)
    return HttpResponse(content)

def multikino( request ):
    return main(request, url='http://multikino.pl/pl/filmy/')

def cinemacity( request ):
    return main(request, url='http://www.cinema-city.pl/index.php?module=movie&action=repertoire')

def searchNew( request, url='http://multikino.pl/pl/filmy/' ):
    added = str( search(url) )
    return HttpResponse( added )

def searchMultikino( request ):
    return searchNew( request, url='http://multikino.pl/pl/filmy/')

def searchCinemacity( request ):
    return searchNew( request, url='http://www.cinema-city.pl/index.php?module=movie&action=repertoire')

def start( request ):
    form = FirstForm()
    return render_to_response( 'start.html', { 'form': form } )

@csrf_exempt
def teach( request ):
    form = FirstForm( request.POST )
    if not form.is_valid():
        return render_to_response( 'start.html', { 'form': form } )

    url = request.POST.get('url', '')
    pole1 = request.POST.get('pole1', '')
    pole2 = request.POST.get('pole2', '')
    pole3 = request.POST.get('pole3', '')
    pole4 = request.POST.get('pole4', '')
    pole5 = request.POST.get('pole5', '')
    pole6 = request.POST.get('pole6', '')

    print url, pole1, pole2, pole3, pole4, pole5, pole6
    return HttpResponse('Zwalidowane')
