from django.core.paginator import Paginator
from django.http import HttpRequest, Http404
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView

from .models import Question, Tag


class MyListView(ListView):
    def paginate_queryset(self, queryset, page_size):  # TODO: paginator over bounds
        try:
            return super().paginate_queryset(queryset, page_size)
        except Http404:
            page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1  # type: str
            self.kwargs[self.page_kwarg] = 1 if int(page) < 1 else 'last'
            return super().paginate_queryset(queryset, page_size)


class QuestionsListView(MyListView):
    template_name = 'questions/list.html'
    model = Question

    paginate_by = 10
    context_object_name = "questions"

    title = "Questions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class QuestionsPopularListView(QuestionsListView):
    title = "Popular"

    def get_queryset(self):
        return Question.objects.popular()


class QuestionsLatestListView(QuestionsListView):
    title = "Latest"

    def get_queryset(self):
        return Question.objects.latest()


class QuestionsByTagListView(QuestionsListView):
    template_name = 'questions/by-tag.html'

    def get_tag(self):
        return Tag.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tag'] = self.get_tag()
        return context

    def get_queryset(self):
        return self.get_tag().questions()


class QuestionDetailView(DetailView):
    template_name = 'questions/detail.html'
    model = Question
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object.answers(), 10)
        page = max(1, min(int(self.request.GET.get('page', 1)), paginator.num_pages))
        page_obj = paginator.get_page(page)  # TODO: paginator over bounds
        context['answers'] = page_obj
        context['is_paginated'] = True

        return context


class AskView(TemplateView):  # TODO: FormView
    template_name = 'questions/ask.html'


def settings(request: HttpRequest):
    return render(request, 'user/settings.html', context={
        'title': 'settings',
    })


def login(request: HttpRequest):
    return render(request, 'user/login.html', context={
        'title': 'login',
    })


def registration(request: HttpRequest):
    return render(request, 'user/registration.html', context={
        'title': 'registration',
    })
