from django.conf.urls import patterns, include, url
from creator import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timetable_creator.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^timetables/', include('creator.urls', namespace="timetable")),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'creator/login.html'}),
    url(r'^log_out/', views.log_out)




)
