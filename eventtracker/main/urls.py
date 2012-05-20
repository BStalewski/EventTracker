from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('main.views',
    (r'^$', 'main'),
    (r'^multi/$', 'multikino'),
    (r'^lastfm/$','lastfm'),
    (r'^cinema/$', 'cinemacity'),
    (r'^search/$', 'searchNew'),
    (r'^search/multi/$', 'searchMultikino'),
    (r'^search/cinema/$', 'searchCinemacity'),
    (r'^start/$', 'start'),
    (r'^teach/$', 'teach'),
)
