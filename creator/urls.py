__author__ = 'annsplit'
from django.conf.urls import patterns, url

from creator import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<conference_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^pdf/(?P<conference_id>[0-9]+)/$', views.create_pdf, name='create_pdf'),
    url(r'^save/$', views.save, name='save'),
    url(r'^edit/(?P<conference_id>[0-9]+)/$', views.edit_report, name='edit'),
    url(r'^change_timecounts/(?P<conference_id>[0-9]+)/$', views.edit_time, name='change_timecounts'),
    url(r'^save_width/$', views.save_width, name='save_width'),
    url(r'^save_height/$', views.save_height, name='save_height'),
    url(r'^save_reports/$', views.save_reports, name='save_reports'),
    url(r'^save_reports_width/$', views.save_reports_width, name='save_reports_width'),
    url(r'^save_reports_height/$', views.save_reports_height, name='save_reports_height'),
    url(r'^data_get/$', views.data_get, name='data_get'),

    # ex: /polls/5/
    #url(r'^(?P<message_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)