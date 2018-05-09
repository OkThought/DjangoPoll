from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import Question


def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_questions': latest_questions}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesnNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    return HttpResponse("Results of question %d" % question_id)


def vote(request, question_id):
    return HttpResponse("Vote question %d" % question_id)
