from django.http import HttpResponse

from .models import Question


def index(request):
    last5questions = Question.objects.order_by('-pub_date')[:5]
    payload = ', '.join([q.question_text for q in last5questions])
    return HttpResponse('Recent questions: %s' % payload)


def detail(request, question_id):
    return HttpResponse("Details of question %d" % question_id)


def results(request, question_id):
    return HttpResponse("Results of question %d" % question_id)


def vote(request, question_id):
    return HttpResponse("Vote question %d" % question_id)
