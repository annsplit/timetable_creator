__author__ = 'annsplit'
from django.conf.urls import patterns, url

from creator import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^save/$', views.save, name='save'),
    url(r'^save_width/$', views.save_width, name='save_width'),
    url(r'^save_height/$', views.save_height, name='save_height'),
    url(r'^save_reports/$', views.save_reports, name='save_reports')

    # ex: /polls/5/
    #url(r'^(?P<message_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)