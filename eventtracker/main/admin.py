from main.models import Person, Place, Event, Style, Obiekt, Url_json
from django.contrib import admin

class ObiektAdmin(admin.ModelAdmin):
    list_display = ('pole1', 'pole2', 'pole3', 'pole4', 'pole5', 'pole6', 'url')

class Url_jsonAdmin(admin.ModelAdmin):
    list_display = ('url', 'json')

admin.site.register(Obiekt, ObiektAdmin)
admin.site.register(Url_json, Url_jsonAdmin)
admin.site.register(Person)
admin.site.register(Place)
admin.site.register(Event)
admin.site.register(Style)
