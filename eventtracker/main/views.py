# Create your views here.

from django.http import HttpResponse
import analyzer

def main( request ):
    content = analyzer.analyze()

    return HttpResponse(content)
