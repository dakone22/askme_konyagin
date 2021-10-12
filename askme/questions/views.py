from os.path import join

from django.shortcuts import render


def index(request):
    context = {
        'title': 'Questions',
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
