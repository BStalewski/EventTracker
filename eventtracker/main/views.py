# Create your views here.

from django.http import HttpResponse
import analyzer
import mk_analyzer

def main( request ):
    content = mk_analyzer.analyze()

    return HttpResponse(content)
