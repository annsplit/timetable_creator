from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import Http404



# Create your views here.
from django.http import HttpResponse

from creator.models import message


def index(request):
    latest_message_list = message.objects.all().order_by('-date')[:5]
    context = {'latest_message_list': latest_message_list}
    return render(request, 'creator/index.html', context)

#def detail(request, poll_id):
 #   poll = get_object_or_404(Poll, pk=poll_id)
  #  return render(request, 'polls/detail.html', {'poll': poll})

#def results(request, poll_id):
 #   return HttpResponse("You're looking at the results of poll %s." % poll_id)

#def vote(request, poll_id):
 #   return HttpResponse("You're voting on poll %s." % poll_id)