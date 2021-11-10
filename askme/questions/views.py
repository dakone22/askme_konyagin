from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from .forms import RegistrationForm, ProfileForm, AskForm
from .models import Question, Tag


class MyListView(ListView):
    def paginate_queryset(self, queryset, page_size):
        try:
            return super().paginate_queryset(queryset, page_size)
        except Http404:
            page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1  # type: str | int
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

        paginator = Paginator(self.object.answers().order_by('date'), 10)  # TODO: filter by votes
        page = max(1, min(int(self.request.GET.get('page', 1)), paginator.num_pages))
        page_obj = paginator.get_page(page)
        context['answers'] = page_obj
        context['is_paginated'] = True

        return context


class AskView(LoginRequiredMixin, FormView):
    template_name = 'questions/ask.html'
    form_class = AskForm

    def form_valid(self, form: AskForm):  # TODO: redirect to new question
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()
        for tag_id in form.data.getlist('tags'):
            tag = Tag.objects.get(pk=int(tag_id))
            question.tags.add(tag)
        question.save()
        return redirect('questions:detail', pk=question.pk)


class RegistrationFormView(View):
    template_name = 'user/registration.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        if 'user_form' not in kwargs:
            kwargs['user_form'] = RegistrationForm()
        if 'password_form' not in kwargs:
            kwargs['password_form'] = SetPasswordForm(None)
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = ProfileForm()
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        u = User()
        user_form = RegistrationForm(request.POST, instance=u)
        password_form = SetPasswordForm(u, request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and password_form.is_valid() and profile_form.is_valid():
            user_form.save()
            password_form.save()
            u.save()
            profile_form2 = ProfileForm(request.POST, request.FILES, instance=u.profile)
            profile_form2.save()

            messages.success(request, 'You have successfully registered!')

            return redirect('user:login')


def settings(request: HttpRequest):
    return render(request, 'user/settings.html', context={
        'title': 'settings',
    })
