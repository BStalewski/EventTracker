from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('main.views',
    (r'$', 'main'),
    (r'multi/$', 'multikino'),
    (r'cinema/$', 'cinemacity'),
)
