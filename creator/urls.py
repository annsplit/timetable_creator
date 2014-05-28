__author__ = 'annsplit'
from django.conf.urls import patterns, url

from creator import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<conference_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^generate/(?P<conference_id>[0-9]+)/$', views.generate_first, name='generate_first'),
    url(r'^pdf/(?P<conference_id>[0-9]+)/$', views.create_pdf, name='create_pdf'),
    url(r'^save/(?P<conference_id>[0-9]+)/$', views.save, name='save'),
    url(r'^edit/(?P<conference_id>[0-9]+)/$', views.edit_report, name='edit'),
    url(r'^change_timecounts/(?P<conference_id>[0-9]+)/$', views.edit_time, name='change_timecounts'),
    url(r'^data_get/(?P<conference_id>[0-9]+)/$', views.data_get, name='data_get'),

    # ex: /polls/5/
    #url(r'^(?P<message_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)