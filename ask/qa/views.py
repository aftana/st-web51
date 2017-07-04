import logging

from models import Question, Answer
from forms import AskForm, AnswerForm, RegistrationForm, LoggingForm

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_GET
from django.contrib.auth import authenticate, login

logger = logging.getLogger('stepic')


def test(request, *args, **kwargs):
    return HttpResponse('OK', status=200)


@require_GET
def main(request):
    new_qas = Question.objects.new()
    paginator, page = paginate(request, new_qas)
    return render(request, 'qa/new_qa.html',
                  {'new_qas': page.object_list,
                   'paginator': paginator,
                   'page': page})


@require_GET
def popular(request):
    popular_qas = Question.objects.popular()
    base_url = '/popular/?page='
    paginator, page = paginate(request, popular_qas, base_url)
    return render(request, 'qa/popular_qa.html',
                  {'popular_qas': page.object_list,
                   'paginator': paginator,
                   'page': page})


def question(request, qa_id):
    qa = get_object_or_404(Question, id=qa_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save()
            user = request.user
            if not user == 'AnonymousUser':
                answer.author = qa.get_user(username=user)
            else:
                answer.author = qa.get_user()
            answer.save()
            return HttpResponseRedirect(qa.get_url())
    else:
        form = AnswerForm(initial={'question': qa})
    return render(request, 'qa/question.html',
                  {'question': qa,
                   'answers': qa.answer_set.all(),
                   'form': form
                   })


def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            qa = form.save()
            user = request.user
            if not user == 'AnonymousUser':
                qa.author = qa.get_user(username=user)
            else:
                qa.author = qa.get_user()
            qa.save()
            return HttpResponseRedirect(qa.get_url())
    else:
        form = AskForm()
    return render(request, 'qa/ask.html', {'form': form})


def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            logger.debug('User_SIGNUP: %s' % user)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'qa/signup.html', {'form': form})


def my_login(request):
    if request.method == 'POST':
        form = LoggingForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                logger.debug('User_LOGIN: %s' % user)
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = LoggingForm()
    return render(request, 'qa/login.html', {'form': form})