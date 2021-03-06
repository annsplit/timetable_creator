# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime, time, date
from django import forms
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.template import RequestContext, loader
from django.forms.formsets import formset_factory
import ConfigParser
import cgi
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from creator.models import report, conference, section, event, section_type
from creator.forms import ReportForm, ReportFormset, TypeForm, TypeFormset, RepTimeForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from datetime import time
import urllib
import urllib2
from urllib2 import urlopen
from urllib import urlencode
import cookielib
import re
import sys
import csv
import traceback
import codecs
from HTMLParser import HTMLParser
pars = HTMLParser()

from django.contrib.auth import authenticate, login
guest = True



def index(request):
    conference_list = conference.objects.order_by('-StartDate')
    template = loader.get_template('creator/base.html')
    usr = True
    if (str(request.user) == "AnonymousUser"):
        usr = False
    context = RequestContext(request, {
        'conference_list': conference_list,
        'usr': usr
    })
    return HttpResponse(template.render(context))


def log_in(request):
    if request.method=="POST":
        username = request.POST['name']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                index(request)
        else:
            return HttpResponse("")
    form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'creator/login.html', context)


from django.contrib.auth import logout
def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login/")


def create_pdf(request, conference_id):
    import reportlab
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import lightgrey, black
    from django.utils import formats
    from reportlab.rl_config import defaultPageSize

    PAGE_WIDTH = defaultPageSize[0]
    PAGE_HEIGHT = defaultPageSize[1]

    def round_to_5(x, base=5):
        return int(base * round(float(x)/base))

    MyFontObject = TTFont('Arial', 'creator/static/creator/arial.ttf')
    pdfmetrics.registerFont(MyFontObject)

    c = conference.objects.get(id=conference_id)
    cname = c.CName

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="timetable.pdf"'
    #wordWrap=True
    p = canvas.Canvas(response)
    p.setFont("Arial",12)
    cname_full = u"Расписание конференции " + '"' + cname + '"'
    header_text_width = cname_full.__len__()*3
    sections = section.objects.filter(Conference=conference_id, StartTime__contains=":").order_by('StartTime')
    if (sections):
        day = formats.date_format(sections[0].StartTime, "DATE_FORMAT")
        print(day)

        #p.setStrokeColor(gray)
        p.drawCentredString(int(PAGE_WIDTH) / 2.0, 820, cname_full)
        #p.drawString((int(PAGE_WIDTH) - header_text_width) / 2.0 - header_text_width/2.0, 820, cname_full)
        p.setFillColor(lightgrey)
        p.rect(0, 780, int(PAGE_WIDTH),20,fill=1)
        p.setFillColor(black)
        p.drawCentredString(int(PAGE_WIDTH) / 2.0, 785, day)
        step=20
        t_format = '%H:%M'

        for s in sections:
            if (day != formats.date_format(s.StartTime, "DATE_FORMAT")):
                if (785-step < 140):
                    p.showPage()
                    step = 20
                    pdfmetrics.registerFont(MyFontObject)
                    p.setFont("Arial",12)
                day = formats.date_format(s.StartTime, "DATE_FORMAT")
                p.setFillColor(lightgrey)
                step = step+40
                p.rect(0, 780-step, int(PAGE_WIDTH),20,fill=1)
                p.setFillColor(black)
                p.drawCentredString(int(PAGE_WIDTH) / 2.0, 785-step, day)
                step = step+17

            st = []

            if (s.Type.TName in [ u"Пленарные", u"Секционные" ]):
                if (785-step < 140):
                    p.showPage()
                    step = 20
                    pdfmetrics.registerFont(MyFontObject)
                    p.setFont("Arial",12)
                st.append(s.SName + " (" + s.Place + ")")
                if s.Person is not None:
                    st.append(u"Председатель: " + s.Person)
                for i in st:
                    text_width = i.__len__()*3
                    p.drawCentredString(int(PAGE_WIDTH) / 2.0, 785- step, i)
                    step = step+17
                events = event.objects.filter(Conference=conference_id, Section_id=s.id).order_by('Section','order')
                #rep_dx = reports_time.objects.get(conference=conference_id)
                if (s.Type.TName == u"Пленарные"):
                    dx = c.plenary
                    q_dx = c.p_questions
                else:
                    dx = c.sectional
                    q_dx = c.s_questions
                count = 0
                current_time = s.StartTime + timedelta(hours=6)
                for e in events:
                    #print(s.id)
                    print(e.Report.RName)
                    pt = []
                    if (e.Report != None):
                        if (e.y_pos == 0.0):
                            t = current_time + timedelta(minutes=dx)
                        else:
                            t = current_time + timedelta(minutes=round_to_5(e.y_pos/2.75))
                        pt.append(current_time.strftime('%H:%M') + " - " + t.strftime('%H:%M') + u" | " + e.Report.RName)
                        sponsor = u" (" + e.Report.Sponsor + u")"
                        pt.append("                        " + e.Report.Author + sponsor)
                        current_time = t
                        t = t + timedelta(minutes=q_dx)
                        pt.append(current_time.strftime('%H:%M') + " - " + t.strftime('%H:%M') + u" | " + u"Ответы на вопросы и обсуждение")
                        current_time = t
                        count = count + 1
                        for i in pt:
                            p.drawString(40, 785-step, i)
                            step = step+17
                        if (785-step < 100):
                            p.showPage()
                            step = 20
                            pdfmetrics.registerFont(MyFontObject)
                            p.setFont("Arial",12)

            else:
                t = s.StartTime + timedelta(hours=6)
                if s.y_pos==0:
                    t_end = s.StartTime + timedelta(minutes=s.Type.time_default) + timedelta(hours=6)
                else:
                    t_end = s.StartTime + timedelta(minutes=round_to_5(s.y_pos/2.75)) + timedelta(hours=6)
                st.append(t.strftime('%H:%M') + " - " + t_end.strftime('%H:%M') + u" | " +  s.SName + " (" + s.Place + ")")
                for i in st:
                    p.drawString(40, 785-step , i)
                    step = step+17
                    if (785-step < 100):
                        p.showPage()
                        step = 20
                        pdfmetrics.registerFont(MyFontObject)
                        p.setFont("Arial",12)
    else:
        p.drawCentredString(int(PAGE_WIDTH) / 2.0, 785, "No sections are avaiable")
    p.showPage()
    p.save()
    return response



@csrf_exempt
@login_required
def edit_report(request, conference_id):
    if request.method=='POST':
        rep = request.POST.items()
        rid=0
        rname=""
        topic = ""
        reporter = ""
        for r in rep:
            if "id" in r[0]:
                rid = r[1]
            if "RName" in r[0]:
                rname = r[1]
            if "Topic" in r[0]:
                topic = r[1]
            if "Reporter" in r[0]:
                reporter = r[1]
        new_rep = report.objects.get(id=int(rid))
        new_rep.RName = rname
        new_rep.Topic = topic
        new_rep.Reporter = reporter
        new_rep.save()
    conference_name = conference.objects.get(id=conference_id)
    qs = report.objects.filter(Conference=conference_id).order_by('-RName')
    if (qs.count()==0):
        formset=None
    else:
        formset = ReportFormset(queryset=qs)
        if formset.is_valid():
            formset.save()
    context = {
        'formset': formset,
        'conference_name': conference_name
    }
    return render(request, 'creator/edit.html', context)


@csrf_exempt
@login_required
def edit_time(request, conference_id):
    conference_name = conference.objects.get(id=conference_id)
    if request.method=='POST':
        time = request.POST.items()
        print(time)
        rst = 0
        rpt = 0
        tid = 0
        tname = ""
        count = ""
        for r in time:
            if "id" in r[0]:
                tid = r[1]
            if "TName" in r[0]:
                tname = r[1]
            if "time_default" in r[0]:
                count = r[1]
            if "sectional" in r[0]:
                rst = r[1]
            if "plenary" in r[0]:
                rpt = r[1]
        if (tid):
            new_t = section_type.objects.get(id=int(tid))
            new_t.TName = tname
            new_t.time_default = count
            new_t.save()
        if (rst != 0):
            #new_t = reports_time.objects.get(conference=conference_id)
            conference_name.sectional = rst
            conference_name.save()
        if (rpt != 0):
            #new_t = reports_time.objects.get(conference=conference_id)
            conference_name.plenary = rpt
            conference_name.save()
    #conference_name = conference.objects.get(id=conference_id)
    qs = section_type.objects.filter(Conference=conference_id).order_by('-TName')
    if (qs.count() == 0):
        formset = None
    else:
        formset = TypeFormset(queryset=qs)
        if formset.is_valid():
            formset.save()
    #rep = reports_time.objects.get(conference=conference_id)
    tform = RepTimeForm(instance=conference_name)
    context = {
        'formset': formset,
        'tform': tform,
        'conference_name': conference_name
    }
    return render(request, 'creator/change_timecounts.html', context)
    #template = loader.get_template('creator/edit.html')
    #context = RequestContext(request, {
    #    'formset': ReportFormset,
    #})
    #return HttpResponse(template.render(context))


def detail(request, conference_id):
    message_list = event.objects.filter(Conference=conference_id).order_by('Section', 'order')
    messagebox_list = report.objects.filter(Conference=conference_id).order_by('Topic')
    topic = messagebox_list.first().Topic
    topic_list = []
    topic_list.append(topic)
    for m in messagebox_list:
        if m.Topic != topic:
            topic = m.Topic
            topic_list.append(topic)
    #types_list = section_type.objects.all()
    conference_name = get_object_or_404(conference, pk=conference_id)

    date_list = []
    diff = conference_name.EndDate - conference_name.StartDate
    date_list.append(conference_name.StartDate)
    for i in range(1, diff.days+1):
        date_list.append(conference_name.StartDate + timedelta(days=i))

    section_list = section.objects.filter(Conference=conference_id).order_by('StartTime')

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



    #form = LoginForm()
    #r = report.objects.get(id=1)
    #form = ReportForm(instance=r)
    #formset = ReportFormset(initial=report)
    #reports_time_list = reports_time.objects.get(conference=conference_id)
    usr = True
    if (str(request.user) == "AnonymousUser"):
        usr = False
    context = {'message_list': message_list,
               'conference_name': conference_name,
               'date_list': date_list,
               #'form': form,
               #'formset':formset,
               'section_list': section_list,
               'time_list': time_list,
               'topic_list': topic_list,
               #'reports_time_list': reports_time_list,
                'usr': usr
    }
    #return render(request, 'creator/detail.html', context)
    return render(request, 'creator/detail.html', context)

@login_required
def generate_first(request, conference_id):
    conf = conference.objects.get(pk=conference_id)
    section.objects.filter(Conference=conf).delete()
    #rt = reports_time.objects.get(conference=conf)
    conf.plenary = 25
    conf.sectional = 15
    conf.p_questions = 5
    conf.s_questions = 5
    conf.save()
    section_type.objects.filter(Conference=conf).delete()

    section_type.objects.create(TName=u"Организационные мероприятия", color="white", time_default=60, Conference=conf)
    section_type.objects.create(TName=u"Обеды", color="ghostwhite", time_default=60, Conference=conf)
    section_type.objects.create(TName=u"Секционные", color="#CEF6D8", time_default=96, Conference=conf)
    section_type.objects.create(TName=u"Пленарные", color="mediumpurple", time_default=106, Conference=conf)
    section_type.objects.create(TName=u"Стендовые", color="#58ACFA", time_default=120, Conference=conf)
    section_type.objects.create(TName=u"Тьюториалы и семинары", color="green", time_default=180, Conference=conf)
    section_type.objects.create(TName=u"Кофе-брейки", color="ghostwhite", time_default=30, Conference=conf)
    section_type.objects.create(TName=u"Выставки", color="#F6D8CE", time_default=120, Conference=conf)
    section_type.objects.create(TName=u"Торжественный ужин", color="#F3E2A9", time_default=120, Conference=conf)

    events_list = event.objects.filter(Conference=conf)
    for e in events_list:
        e.Section = None
        e.y_pos = 0
        e.x_pos = 350
        e.save()

    diff = conf.EndDate - conf.StartDate
    day = conf.StartDate

    for i in range(0, diff.days+1):
        if i == 0:
            section.objects.create(SName=u"Тьюториал", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Тьюториалы и семинары"), StartTime=datetime.combine(day,time(13,0)), x_pos=300)
            section.objects.create(SName=u"Семинар", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Тьюториалы и семинары"), StartTime=datetime.combine(day,time(17,0)), x_pos=300)
            section.objects.create(SName=u"Регистрация участников", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Организационные мероприятия"), StartTime=datetime.combine(day,time(9,0)), y_pos=1172, x_pos=300)
            section.objects.create(SName=u"Обед", Conference=conf, Place=u"Столовая", Type=section_type.objects.get(TName=u"Обеды"), StartTime=datetime.combine(day,time(14,0)), x_pos=300)
        elif i == 2:
            section.objects.create(SName=u"Пленарные доклады", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Пленарные"), StartTime=datetime.combine(day,time(10,0)))
            section.objects.create(SName=u"Кофе-брейк", Conference=conf, Place=u"Столовая", Type=section_type.objects.get(TName=u"Кофе-брейки"), StartTime=datetime.combine(day,time(11,30)))
            section.objects.create(SName=u"Пленарные доклады", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Пленарные"), StartTime=datetime.combine(day,time(12,0)))
            section.objects.create(SName=u"Фотографирование участников конференции", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Организационные мероприятия"), StartTime=datetime.combine(day,time(13,30)), y_pos=83)
            section.objects.create(SName=u"Выставка", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Выставки"), StartTime=datetime.combine(day,time(15,0)), x_pos=300)
            section.objects.create(SName=u"Секция стендовых докладов", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Стендовые"), StartTime=datetime.combine(day,time(15,0)), x_pos=300)
            section.objects.create(SName=u"Торжественный ужин", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Торжественный ужин"), StartTime=datetime.combine(day,time(18,0)))
            section.objects.create(SName=u"Обед", Conference=conf, Place=u"Столовая", Type=section_type.objects.get(TName=u"Обеды"), StartTime=datetime.combine(day,time(14,0)))
        elif i == diff.days:
            section.objects.create(SName=u"Пленарные доклады", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Пленарные"), StartTime=datetime.combine(day,time(10,0)))
            section.objects.create(SName=u"Кофе-брейк", Conference=conf, Place=u"Столовая", Type=section_type.objects.get(TName=u"Кофе-брейки"), StartTime=datetime.combine(day,time(11,30)))
            section.objects.create(SName=u"Секция A", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Секционные"), StartTime=datetime.combine(day,time(12,0)))
            section.objects.create(SName=u"Секция B", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Секционные"), StartTime=datetime.combine(day,time(12,0)))
            section.objects.create(SName=u"Секция A", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Секционные"), StartTime=datetime.combine(day,time(15,30)))
            section.objects.create(SName=u"Молодежная сессия", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Секционные"), StartTime=datetime.combine(day,time(15,30)))
            section.objects.create(SName=u"Кофе-брейк", Conference=conf, Place=u"Столовая", Type=section_type.objects.get(TName=u"Кофе-брейки"), StartTime=datetime.combine(day,time(17,0)))
            section.objects.create(SName=u"Закрытие конференции", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Организационные мероприятия"), StartTime=datetime.combine(day,time(18,0)))
            section.objects.create(SName=u"Обед", Conference=conf, Place=u"Столовая", Type=section_type.objects.get(TName=u"Обеды"), StartTime=datetime.combine(day,time(14,0)))
        elif i == diff.days+1:
            section.objects.create(SName=u"Торжественное закрытие конференции", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Организационные мероприятия"), StartTime=datetime.combine(day,time(18,0)))
            section.objects.create(SName=u"Фотографирование", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Организационные мероприятия"), StartTime=datetime.combine(day,time(19,0)))
            section.objects.create(SName=u"Обед", Conference=conf, Place=u"Столовая", Type=section_type.objects.get(TName=u"Обеды"), StartTime=datetime.combine(day,time(14,0)))
        else:
            section.objects.create(SName=u"Регистрация участников", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Организационные мероприятия"), StartTime=datetime.combine(day,time(9,0)))
            section.objects.create(SName=u"Пленарные доклады", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Пленарные"), StartTime=datetime.combine(day,time(10,15)))
            section.objects.create(SName=u"Кофе-брейк", Conference=conf, Place=u"Столовая", Type=section_type.objects.get(TName=u"Кофе-брейки"), StartTime=datetime.combine(day,time(11,45)))
            section.objects.create(SName=u"Пленарные доклады", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Пленарные"), StartTime=datetime.combine(day,time(12,15)))
            section.objects.create(SName=u"Секция A", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Секционные"), StartTime=datetime.combine(day,time(16,0)))
            section.objects.create(SName=u"Секция B", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Секционные"), StartTime=datetime.combine(day,time(16,0)))
            section.objects.create(SName=u"Кофе-брейк", Conference=conf, Place=u"Столовая", Type=section_type.objects.get(TName=u"Кофе-брейки"), StartTime=datetime.combine(day,time(17,20)))
            section.objects.create(SName=u"Секция A", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Секционные"), StartTime=datetime.combine(day,time(17,50)))
            section.objects.create(SName=u"Молодежная сессия", Conference=conf, Place=u"Установите место", Type=section_type.objects.get(TName=u"Секционные"), StartTime=datetime.combine(day,time(17,50)))
            section.objects.create(SName=u"Обед", Conference=conf, Place=u"Столовая", Type=section_type.objects.get(TName=u"Обеды"), StartTime=datetime.combine(day,time(14,0)))
        day = day + timedelta(days=1)

    section_list = section.objects.filter(Conference=conf)
    for s in section_list:
        if s.Type.TName == u"Пленарные":
            for i in range(1, 4):
                e = event.objects.filter(Conference=conf, Section=None).order_by('Report__Topic').last()
                if e is not None:
                    e.Section = s
                else:
                    e = event.objects.create(Section=s, Conference=conf)
                e.y_pos = (conf.plenary + conf.p_questions) * 2.75
                e.x_pos = 350
                e.save()
        if s.Type.TName == u"Секционные":
            s.x_pos = 360
            s.save()
            for i in range(1, 5):
                e = event.objects.filter(Conference=conf, Section=None).order_by('Report__Topic').last()
                if e is not None:
                    e.Section = s
                else:
                    e = event.objects.create(Section=s, Conference=conf)
                e.y_pos = (conf.sectional + conf.s_questions) * 2.75
                e.x_pos = 350
                e.save()


    return HttpResponseRedirect("/timetables/" + conference_id)


@login_required
@csrf_exempt
def save(request, conference_id):
    import json
    if request.method == 'POST':
        changes = json.loads(request.body)
        param = "%Y-%m-%d %H:%M"
        conf = conference.objects.get(id=conference_id)
        section_list = section.objects.filter(Conference=conf)
        for s in section_list:
            for sect in changes["positions"]:
                if int(sect) == s.id:
                    if changes["positions"][sect] == "":
                        newtime = None
                    else:
                        newtime = datetime.strptime(changes["positions"][sect], param)
                    s.StartTime = newtime
            for wid in changes["width"]:
                if wid[0] == "s":
                    if int(wid[1:]) == s.id:

                        s.x_pos = changes["width"][wid][:-2]
            for hei in changes["height"]:
                if hei[0] == "s":
                    if int(hei[1:]) == s.id:
                        s.y_pos = changes["height"][hei][:-2]
            print(s.id)
            s.save()

        event_list = event.objects.filter(Conference=conf)
        for e in event_list:
            for wid in changes["width"]:
                if wid[0] == "r":
                    print(wid)
                    if int(wid[1:]) == e.id:
                        print(int(wid[1:]))
                        e.x_pos = changes["width"][wid][:-2]
            for hei in changes["height"]:
                if hei[0] == "r":
                    if int(hei[1:]) == e.id:
                        e.y_pos = changes["height"][hei][:-2]

            is_changed = False
            sect = ""
            for o in changes["order"]:
                s_order = changes["order"][o].split("&")
                count = 0
                for item in s_order:
                    r_id = item[4:]
                    if "s" not in r_id:
                        if int(r_id) == e.id:
                            print(s_order)
                            e.order = count
                            e.save()
                            is_changed = True
                            sect = s_order[0][4:]
                        count = count + 1
            if not is_changed:
                e.Section = None
            else:
                e.Section = section.objects.get(id=int(sect[3:]))
            print(e.id)
            e.save()
    return HttpResponse('Success')


@login_required
def change_timecount(request):
    time_list = section_type.objects.all()
    return render(request, 'creator/change_timecounts.html', {'time_list': time_list} )

#def detail(request, conference_id):
 #   poll = get_object_or_404(conference, pk=conference_id)
  #  return render(request, 'polls/detail.html', {'poll': poll})

#def results(request, poll_id):
 #   return HttpResponse("You're looking at the results of poll %s." % poll_id)

#def vote(request, poll_id):
 #   return HttpResponse("You're voting on poll %s." % poll_id)

url = u'http://newserv.srcc.msu.ru/PMA/'


def unescape_entities(s):
    escaped = s
    unescaped = pars.unescape(escaped)
    while (unescaped != escaped):
        escaped = unescaped
        unescaped = pars.unescape(escaped)
    return unescaped


import os
#name = os.path.dirname(os.path.dirname(__file__)) +"\config.ini"
#Config = ConfigParser.ConfigParser()
#f = open(name, 'rb')
#f.readline()
#Config.readfp(f)


#authorstable = u"conf_pavt2014_appl_members"
#reportstable = u"conf_pavt2014_thes_reports"
#expertstable = u"conf_pavt2014_experts"

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
        u'csv_separator': u'|',
        u'csv_enclosed': u'',
        u'csv_escaped': u'\\',
        u'csv_terminated': u'$$\n',
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
    f = codecs.open(filename, u'w', encoding=outenc, errors=u'replace')
    print u'replacing entities'
    csv = unescape_entities(csv)
    f.write(csv)
    f.close()
    print u"table '%s' saved to file '%s'" % (table, filename)

def now():
    return datetime.now().strftime(u'%Y%m%d%H%M%S')

@login_required
def data_get(request, conference_id):
    conference_name = conference.objects.get(id=conference_id)
    authorstable = conference_name.authors_table
    reportstable = conference_name.reports_table
    lgn = conference_name.login
    psswd = conference_name.password
    (username, password) = (lgn, psswd)
    db = conference_name.database

    #database = db
    try:
        init_cookie_jar()
        if not login(username, password):
            sys.exit(1)

        files = {}
        for table in [authorstable, reportstable]:
            filename = '%s-%s.csv' % (table, now())
            table_to_csv(table, filename)
            files[table] = filename

        #csv.register_dialect('unixpwd', delimiter=':', quoting=csv.QUOTE_NONE)
        #print(files[1])
        #with open(files[1]) as f:
         #   reader = csv.reader(f, delimiter='|', lineterminator='$\n', enclosechar='}')
        #for row in reader:
         #   print row
        filenames = list(files.values())

        def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
            # csv.py doesn't do Unicode; encode temporarily as UTF-8:
            csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),   **kwargs)
            for row in csv_reader:
                # decode UTF-8 back to Unicode, cell by cell:
                yield [unicode(cell, 'utf-8') for cell in row]

        def utf_8_encoder(unicode_csv_data):
            for line in unicode_csv_data:
                yield line.encode('utf-8')


        #f = codecs.open(filenames[1], u'rb', encoding=u'koi8-r', errors=u'replace')
        #with codecs.open(filenames[1], u'w', encoding=u'cp1251', errors=u'replace') as f:
        def records(path):
            with codecs.open(path, 'rbU', encoding='cp1251', errors=u'replace') as f:
                contents = f.read().replace('\n', '').replace('\r', '')
                return (record for record in contents.split('$$'))

        #clean = codecs.open(filenames[1], 'rbU', encoding=u'koi8-r', errors=u'replace').read().replace('\n', '')
        reader_a = unicode_csv_reader(records(filenames[1]),  delimiter='|', lineterminator='$$')
        reader_r = unicode_csv_reader(records(filenames[0]),  delimiter='|', lineterminator='$$')

        authors = []
        header = []
        rownum = 0
        for row in reader_a:
            if rownum == 0:
                header = row
                print(header)
                rownum+=1
            else:
                colnum = 0
                aid = u""
                surname = u""
                name = u""
                patronymic = u""
                organisation = u""
                sponsor = u""
                for col in row:
                    if header[colnum] == 'id':
                        aid = col
                        #print(col)
                    if header[colnum] == 'familiya':
                        surname = col
                    elif header[colnum] == 'imya':
                        name = col
                    elif header[colnum] == 'otchestvo':
                        patronymic = col
                    elif header[colnum] == 'afield020':
                        sponsor = col
                        new_author = [aid, name[:1] + u"." + patronymic[:1] + u". " + surname, organisation, sponsor]
                        authors.append(new_author)
                    elif header[colnum] == 'afield001':
                        organisation = col
                    colnum +=1


        header = []
        rownum = 0
        for row in reader_r:
            if rownum == 0:
                header = row
                #print(header)
                rownum+=1
            else:
                colnum = 0
                rid = u""
                title = u""
                ann = u""
                reporter = u""
                topic = u""
                session = u""
                author = u""
                final = u""
                organisation = u""
                sponsor = u""

                for col in row:
                    if header[colnum] == 'id':
                        rid = col
                        #print(col)
                    if header[colnum] == 'title':
                        title = col
                    elif header[colnum] == 'xfield001':
                        ann = col
                    elif header[colnum] == 'xfield008':
                        reporter = col
                    elif header[colnum] == 'xfield016':
                        topic = col
                        if author == "":
                            reporter_split = reporter.split(u" ")
                            author = reporter_split[1][0] + u"." + reporter_split[2][0] + u". " + reporter_split[0]
                        if report.objects.filter(rid=int(rid), Conference=conference_name).count() == 0:
                            rep = report(rid=int(rid), RName=title, Annotation=ann, Reporter=reporter, Topic=topic, Session=session, Organisation=organisation, Author=author, Sponsor=sponsor, IsFinal=final, Conference=conference_name )
                            rep.save()
                            ev = event(Conference=conference_name, Report=rep)
                            ev.save()
                    elif header[colnum] == 'xfield005':
                        session = col
                    elif header[colnum] == 'authors':
                        authors_ids = col
                        for a in authors:
                            if u"." + str(a[0]) + u"." in authors_ids:
                                if author =="":
                                    author = a[1]
                                else:
                                    author = author + ", " + a[1]
                                organisation = a[2]
                                if u"понсор" in a[3]:
                                    sponsor = organisation
                                else:
                                    sponsor = ""
                    elif header[colnum] == 'confirm':
                        final = col


                    colnum +=1
                #print rid,title,ann,reporter,topic,session,author,final

                #print(col)
                #rep = report(rid=int(rid), RName=title, Annotation=ann, Reporter=reporter, Topic=topic, Session=session, Organisation='unknown', Author=author, Sponsor='unknown', IsFinal=final )
                #rep.save()
                    #new_report.append(col.encode('utf-8'))
                    #print new_report[0][1]
                    #rep = report(id=)

        #print(dictionary)



        print u'done.'
    except Exception, e:
        print u'FAILURE: %s' % e
        traceback.print_exc()
        print u'Dying!'
        sys.exit(1)

    return HttpResponseRedirect("/timetables/")