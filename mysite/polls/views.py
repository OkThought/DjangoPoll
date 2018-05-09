from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest5 = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_questions': latest5,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    return HttpResponse("Details of question %d" % question_id)


def results(request, question_id):
    return HttpResponse("Results of question %d" % question_id)


def vote(request, question_id):
    return HttpResponse("Vote question %d" % question_id)
