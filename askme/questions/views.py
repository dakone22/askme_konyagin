from os.path import join

from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render


def paginate(objects_list: list, request: HttpRequest, per_page=10):
    paginator = Paginator(objects_list, per_page)
    n = max(1, min(int(request.GET.get('page', 1)), paginator.num_pages))
    page_obj = paginator.get_page(n)

    return page_obj


def index(request):
    context = {
        'title': 'Questions',
        'questions': paginate([
            {'title': f'Title{i}', 'text': f'Text{i}'} for i in range(50)
        ], request),
    }
    return render(request, join('index.html'), context)


def ask(request):
    context = {
        'title': 'ask',
    }
    return render(request, join('ask.html'), context)


def question(request, question_id):
    context = {
        'title': str(question_id),
    }
    return render(request, join('question.html'), context)


def tag(request, tag):
    context = {
        'title': tag,
    }
    return render(request, join('tag.html'), context)


def settings(request):
    context = {
        'title': 'settings',
    }
    return render(request, join('settings.html'), context)


def login(request):
    context = {
        'title': 'login',
    }
    return render(request, join('login.html'), context)


def registration(request):
    context = {
        'title': 'registration',
    }
    return render(request, join('registration.html'), context)
