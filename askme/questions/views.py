import os

from django.shortcuts import render

from .models import Question, Tag


# class MyTemplateView(TemplateView):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['latest_articles'] = Article.objects.all()[:5]
#         return context


def index(request):
    context = {
        'title': 'Questions',
        'questions': Question.objects.all(),
        'top_tags': Tag.objects.top(),
    }
    return render(request, os.path.join('index.html'), context)


def ask(request):
    context = {
        'title': 'ask',
    }
    return render(request, os.path.join('ask.html'), context)


def question(request, question_id):
    context = {
        'title': str(question_id),
        'question': Question.objects.get(id=question_id),
    }
    return render(request, os.path.join('question.html'), context)


def tag(request, tag):
    context = {
        'title': tag,
        'tag': Tag.objects.get(pk=tag),
    }
    return render(request, os.path.join('tag.html'), context)


def settings(request):
    context = {
        'title': 'settings',
    }
    return render(request, os.path.join('settings.html'), context)


def login(request):
    context = {
        'title': 'login',
    }
    return render(request, os.path.join('login.html'), context)


def registration(request):
    context = {
        'title': 'registration',
    }
    return render(request, os.path.join('registration.html'), context)
