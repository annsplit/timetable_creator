from django.shortcuts import render
from datetime import timedelta, datetime, time, date
from django import forms

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import Http404



# Create your views here.
from django.http import HttpResponse, QueryDict
from creator.models import report, conference, section
from django.views.decorators.csrf import csrf_exempt
from datetime import time
import urllib


class LoginForm(forms.Form):
    username = forms.CharField(label=u'name')
    password = forms.CharField(label=u'pass', widget=forms.PasswordInput())


def index(request):
    message_list = report.objects.all().order_by('-RName')

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
            if (positions[p] > 0):
                rep = report.objects.get(id=p)
                newpos = positions[p]
                rep.SID_id = newpos
                rep.save(update_fields=['SID_id'])
    return HttpResponse('Success')

#def detail(request, poll_id):
 #   poll = get_object_or_404(Poll, pk=poll_id)
  #  return render(request, 'polls/detail.html', {'poll': poll})

#def results(request, poll_id):
 #   return HttpResponse("You're looking at the results of poll %s." % poll_id)

#def vote(request, poll_id):
 #   return HttpResponse("You're voting on poll %s." % poll_id)