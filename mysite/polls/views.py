from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, question_id):
    return HttpResponse("Details of question %d" % question_id)


def results(request, question_id):
    return HttpResponse("Results of question %d" % question_id)


def vote(request, question_id):
    return HttpResponse("Vote question %d" % question_id)
