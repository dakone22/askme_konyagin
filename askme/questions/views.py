import os

from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render

from .models import Question, Tag


def get_page_object(request: HttpRequest, objects: list, count_on_list=5, adjacent_pages=2):
    paginator = Paginator(objects, count_on_list)
    n = request.GET.get('page')
    page_obj = paginator.get_page(n)

    if int(n) < 1:
        page_obj.number = 1
    if page_obj.number > paginator.num_pages:
        page_obj.number = paginator.num_pages

    start_page = max(page_obj.number - adjacent_pages, 1)
    if start_page <= 3:
        start_page = 1
    end_page = page_obj.number + adjacent_pages + 1
    if end_page >= paginator.num_pages - 1:
        end_page = paginator.num_pages + 1

    page_numbers = [n for n in range(start_page, end_page) if n in range(1, paginator.num_pages + 1)]

    page_obj.page_numbers = page_numbers
    page_obj.show_first = 1 not in page_numbers
    page_obj.show_last = paginator.num_pages not in page_numbers

    return page_obj


def index(request: HttpRequest):
    return render(request, 'question-list.html', context={
        'title': 'Questions',
        'questions': get_page_object(request, Question.objects.all()),
    })


def popular(request: HttpRequest):
    return render(request, 'question-list.html', context={
        'title': 'Questions',
        'questions': get_page_object(request, Question.objects.popular()),
    })


def latest(request: HttpRequest):
    return render(request, 'question-list.html', context={
        'title': 'Latest',
        'questions': get_page_object(request, Question.objects.latest()),
    })


def ask(request: HttpRequest):
    return render(request, 'ask.html', context={
        'title': 'ask',
    })


def question(request, question_id):
    q = Question.objects.get(id=question_id)
    return render(request, os.path.join('question.html'), context={
        'title': str(question_id),
        'question': q,
        'answers': get_page_object(request, q.answers()),
    })


def tag(request, tag):
    return render(request, 'tag.html', context={
        'title': tag,
        'tag': Tag.objects.get(pk=tag),
    })


def settings(request: HttpRequest):
    return render(request, 'settings.html', context={
        'title': 'settings',
    })


def login(request: HttpRequest):
    return render(request, 'login.html', context={
        'title': 'login',
    })


def registration(request: HttpRequest):
    return render(request, 'registration.html', context={
        'title': 'registration',
    })
