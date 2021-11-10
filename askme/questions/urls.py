from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

from . import views

questions_urls = ([
    path('list/', views.QuestionsListView.as_view(), name='list'),
    path('popular/', views.QuestionsPopularListView.as_view(), name='popular'),
    path('latest/', views.QuestionsLatestListView.as_view(), name='latest'),
    path('tag/<slug:slug>/', views.QuestionsByTagListView.as_view(), name='by-tag'),

    path('ask/', views.AskView.as_view(), name='ask'),

    path('<int:pk>/', views.QuestionDetailView.as_view(), name='detail'),
], 'questions')

user_urls = ([
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', views.RegistrationFormView.as_view(), name='registration'),
    path('settings/', views.settings, name='settings'),
    path('reset/', TemplateView.as_view(template_name='base/index.html'), name='password_reset'),  # TODO
], 'user')


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='questions:list'), name='index'),
    path('questions/', include(questions_urls)),
    path('user/', include(user_urls)),
]
