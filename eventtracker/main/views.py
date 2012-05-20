# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from universal_analyzer import teach
from search import search
from forms import *
from models import Obiekt, Url_json

# url: /main/
def main(request, url='http://multikino.pl/pl/filmy/'):
    obj = Obiekt.objects.filter(url=url)[0]
    content = teach(url, obj.key1, obj.key2)
    return HttpResponse(content)

# url: /main/multi/
def multikino(request):
    return main(request, url='http://multikino.pl/pl/filmy/')

# url: /main/cinema/
def cinemacity(request):
    return main(request, url='http://www.cinema-city.pl/index.php?module=movie&action=repertoire')

# url: /main/search/
def searchNew(request, url='http://multikino.pl/pl/filmy/'):
    added = str( search(url) )
    return HttpResponse(added)

# url: /main/search/multi/
def searchMultikino(request):
    return searchNew(request, url='http://multikino.pl/pl/filmy/')

# url: /main/search/cinema/
def searchCinemacity(request):
    return searchNew(request, url='http://www.cinema-city.pl/index.php?module=movie&action=repertoire')

# with user interface

# url: /start/
def start(request):
    form = ObjectForm()
    return render_to_response( 'start.html', { 'form': form } )

# url: /teach/
@csrf_exempt
def teachData(request):
    form = ObjectForm(request.POST)
    if not form.is_valid():
        return render_to_response( 'start.html', { 'form': form } )

    url = request.POST.get('url', '')
    key1 = request.POST.get('pole1', '')
    key2 = request.POST.get('pole2', '')
    key3 = request.POST.get('pole3', '')
    key4 = request.POST.get('pole4', '')
    key5 = request.POST.get('pole5', '')
    key6 = request.POST.get('pole6', '')

    if Obiekt.objects.filter(url=url, pole1=key1, pole2=key2, pole3=key3, pole4=key4, pole5=key5, pole6=key6).count() > 0:
        return HttpResponse('Podane dane juz w bazie')
    else:
        newObject = Obiekt(url=url, pole1=key1, pole2=key2, pole3=key3, pole4=key4, pole5=key5, pole6=key6)
        newObject.save()
        teachResult = teach(url, key1, key2)
        try:
            urlJson, foundUrl = teachResult
        except:
            return HttpResponse('Nie znaleziono zadnej sciezki w serwisie %s' % url)

        paths = {
            'path1': urlJson[0],
            'path2': urlJson[1],
            'path3': urlJson[2],
            'path4': urlJson[3],
            'path5': urlJson[4],
            'path6': urlJson[5]
        }
        form = PathsForm(paths)
        return render_to_response('path.html', {'form': form, 'urlurl': foundUrl})

# url: /others/
def others(request):
    form = TeachForm()
    return render_to_response('others.html', { 'form': form })

# url: /show/
@csrf_exempt
def showOthers(request):
    url = request.POST.get('url', '')
    try:
        limit = int( request.POST.get('limit', '') )
    except:
        limit = None
    added = search(url, limit)
    formset = ResultFormset(initial=added)
    info = {
        'header': 'Wyszukane informacje z portalu',
        'url': url,
        'formset': formset
    }
    return render_to_response('show.html', info)

# url: /acutal/
def actual(request):
    form = UrlForm()
    return render_to_response('actual.html', { 'form': form })

# url: /showactual/
@csrf_exempt
def showActual(request):
    url = request.POST.get('url', '')
    results = Obiekt.objects.filter(url=url).values()
    formset = ResultFormset(initial=results)
    info = {
        'header': 'Wszystkie informacje z portalu',
        'url': url,
        'formset': formset
    }
    return render_to_response('show.html', info)

