from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import Http404



# Create your views here.
from django.http import HttpResponse

from creator.models import report, conference


def index(request):
    message_list = report.objects.all().order_by('-RName')
    conference_name = conference.objects.first()
    context = {'message_list': message_list,
               'conference_name': conference_name
    }
    return render(request, 'creator/index.html', context)

#def detail(request, poll_id):
 #   poll = get_object_or_404(Poll, pk=poll_id)
  #  return render(request, 'polls/detail.html', {'poll': poll})

#def results(request, poll_id):
 #   return HttpResponse("You're looking at the results of poll %s." % poll_id)

#def vote(request, poll_id):
 #   return HttpResponse("You're voting on poll %s." % poll_id)