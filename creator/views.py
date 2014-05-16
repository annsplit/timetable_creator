from django.shortcuts import render
from datetime import timedelta, datetime, time, date
from django import forms

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import Http404



# Create your views here.
from django.http import HttpResponse, QueryDict
from creator.models import report, conference, section, event
from django.views.decorators.csrf import csrf_exempt
from datetime import time
import urllib
import urllib2
from urllib2 import urlopen
from urllib import urlencode
import cookielib
import re
import sys
import datetime
import traceback
import codecs

from HTMLParser import HTMLParser
pars = HTMLParser()


class LoginForm(forms.Form):
    username = forms.CharField(label=u'name')
    password = forms.CharField(label=u'pass', widget=forms.PasswordInput())


def index(request):
    message_list = event.objects.all().order_by('-Report')

    conference_name = conference.objects.first()

    date_list = []
    diff = conference_name.EndDate - conference_name.StartDate
    date_list.append(conference_name.StartDate)
    for i in range(1, diff.days+1):
        date_list.append(conference_name.StartDate + timedelta(days=i))

    section_list = section.objects.all().order_by('StartTime')

    time_list = []
    start = conference_name.DayStart.strftime('%H:%M')
    stop = conference_name.DayEnd.strftime('%H:%M')

    hours_begin = int(start.split(':')[0]) # 01
    minutes_begin = int(start.split(':')[1]) # 45
    hours_end = int(stop.split(':')[0]) # 05
    minutes_end = int(stop.split(':')[1]) # 30
    total_minutes = (hours_end - hours_begin) * 60 + minutes_end - minutes_begin

    time_list.append(conference_name.DayStart)
    for i in range(5, total_minutes+1, 5):
        time_list.append((datetime.combine(date.today(), conference_name.DayStart) + timedelta(minutes=i)).time())


    form = LoginForm()

    context = {'message_list': message_list,
               'conference_name': conference_name,
               'date_list': date_list,
               'form': form,
               'section_list': section_list,
               'time_list': time_list

    }
    return render(request, 'creator/index.html', context)


@csrf_exempt
def save(request):
    if request.method == 'POST':
        times = request.POST
        for t in times:
            my = section.objects.get(id=t)
            param = "%Y-%m-%d %H:%M:%S"
            if (times[t] == ""):
                newtime = None
            else:
                newtime = datetime.strptime(times[t], param)
            my.StartTime = newtime
            my.save(update_fields=['StartTime'])
    return HttpResponse('Success')

@csrf_exempt
def save_width(request):
    if request.method == 'POST':
        width = request.POST
        for w in width:
            if (width[w] > 0):
                sect = section.objects.get(id=w)
                newwidth = width[w]
                sect.x_pos = newwidth
                sect.save(update_fields=['x_pos'])
    return HttpResponse('Success')


@csrf_exempt
def save_height(request):
    if request.method == 'POST':
        height = request.POST
        for h in height:
            if (height[h] > 0):
                sect = section.objects.get(id=h)
                newheight = height[h]
                sect.y_pos = newheight
                sect.save(update_fields=['y_pos'])
    return HttpResponse('Success')


@csrf_exempt
def save_reports(request):
    if request.method == 'POST':
        positions = request.POST
        for p in positions:
            rep = event.objects.get(id=p)
            if (positions[p] > '0'):
                newpos = positions[p]
            else:
                newpos = None;
            if (rep.Section_id != newpos):
                rep.Section_id = newpos
                rep.save(update_fields=['Section_id'])
    return HttpResponse('Success')


@csrf_exempt
def save_reports_width(request):
    if request.method == 'POST':
        width = request.POST
        for w in width:
            if (width[w] > 0):
                rep = event.objects.get(id=w)
                newwidth = width[w]
                rep.y_pos = newwidth
                rep.save(update_fields=['x_pos'])
    return HttpResponse('Success')


@csrf_exempt
def save_reports_height(request):
    if request.method == 'POST':
        height = request.POST
        for h in height:
            if (height[h] > 0):
                rep = event.objects.get(id=h)
                newheight = height[h]
                rep.y_pos = newheight
                rep.save(update_fields=['y_pos'])
    return HttpResponse('Success')
#def detail(request, poll_id):
 #   poll = get_object_or_404(Poll, pk=poll_id)
  #  return render(request, 'polls/detail.html', {'poll': poll})

#def results(request, poll_id):
 #   return HttpResponse("You're looking at the results of poll %s." % poll_id)

#def vote(request, poll_id):
 #   return HttpResponse("You're voting on poll %s." % poll_id)


def unescape_entities(s):
    escaped = s
    unescaped = pars.unescape(escaped)
    while (unescaped != escaped):
        escaped = unescaped
        unescaped = pars.unescape(escaped)
    return unescaped


(username, password) = ("pavt2014", "hjcnjd")
url = u'http://newserv.srcc.msu.ru/PMA/'
database = u"agora"
authorstable = u"conf_pavt2014_appl_members"
reportstable = u"conf_pavt2014_thes_reports"
expertstable = u"conf_pavt2014_experts"

def init_cookie_jar():
    global jar
    jar = cookielib.MozillaCookieJar(u'cookies.txt')

    try:
        print u"trying to load cookies"
        jar.load()
        print u"cookies loaded"
    except:
        print u"cannot load cookies, overwriting the file with empty cookies"
        jar.save()

    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(jar)))

def need_to_login():
    page = urlopen(url + u'index.php').read().decode(u'latin1')
    return ur'<body class="loginform">' in page

def postencode(**kwargs):
    return urlencode(kwargs).encode(u'latin1')

def login(username, password):
    global jar
    if need_to_login():
        print u"need to log in"
    else:
        print u"already logged in"
        jar.save()
        return True

    global token
    page = urlopen(url, postencode(pma_username=username, pma_password=password)).read().decode(u'latin1')
    m = re.search(ur'token=(\w+)', page, re.MULTILINE)
    if m:
        token = m.group(1)
        print u'token = "%s"' % token
    else:
        print u'cannot parse token'
        return False

    if need_to_login():
        print u"failed to log in"
        return False
    else:
        print u"logged in"
        jar.save()
        return True

def table_to_csv(table, filename, inenc=u'koi8-r', outenc=u'cp1251'):
    print u"saving table '%s' (%s) to file '%s' (%s)" % (table, inenc, filename, outenc)
    postdata = {
        u'db': u'agora',
        u'table': table,
        u'token': token,
        u'single_table': u'TRUE',
        u'export_type': u'table',
        u'what': u'csv',
        u'csv_data': u'',
        u'csv_separator': u'$',
        u'csv_enclosed': u'}',
        u'csv_escaped': u'\\',
        u'csv_terminated': u'AUTO',
        u'csv_null': u'',
        u'csv_columns': u'something',
        u'asfile': u'sendit',
		u'filename_template': u'__TABLE__',
		u'compression': u'none',
	}
    print u"query: %s" % repr(postdata)
    encdata = postencode(**postdata)
    print u"encoded query: %s" % encdata
    csv = urlopen(url + u'export.php', encdata).read().decode(u'koi8-r')
    #f = open(filename, u'w', encoding=outenc, errors=u'replace')
    f = codecs.open(filename, u'w', encoding=outenc, errors=u'replace')
    print u'replacing entities'
    csv = unescape_entities(csv)
    f.write(csv)
    print u"table '%s' saved to file '%s'" % (table, filename)

def now():
    return datetime.datetime.now().strftime(u'%Y%m%d%H%M%S')

def data_get(request):
    try:
        init_cookie_jar()
        if not login(username, password):
            sys.exit(1)

        files = {}
        for table in [authorstable, reportstable, expertstable]:
            filename = '%s-%s.csv' % (table, now())
            table_to_csv(table, filename)
            files[table] = filename

        filenames = list(files.values())



        print u'done.'
    except Exception, e:
        print u'FAILURE: %s' % e
        traceback.print_exc()
        print u'Dying!'
        sys.exit(1)

    return HttpResponse('okay')