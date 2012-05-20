from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('main.views',
    (r'^main/$', 'main'),
    (r'^main/multi/$', 'multikino'),
    (r'^main/lastfm/$', 'lastfm'),
    (r'^main/cinema/$', 'cinemacity'),
    (r'^main/search/$', 'searchNew'),

    (r'^main/search/multi/$', 'searchMultikino'),
    (r'^main/search/cinema/$', 'searchCinemacity'),

    (r'^start/$', 'start'),
    (r'^teach/$', 'teachData'),

    (r'^others/$', 'others'),
    (r'^show/$', 'showOthers'),
    (r'^actual/$', 'actual'),
    (r'^showactual/$', 'showActual'),
)
