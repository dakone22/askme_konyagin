from django.urls import path, include
from django.views.generic import RedirectView

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
        path('login/', views.login, name='login'),
        path('registration/', views.registration, name='registration'),
        path('settings/', views.settings, name='settings'),
], 'user')


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='questions:list'), name='index'),
    path('questions/', include(questions_urls)),
    path('user/', include(user_urls)),
]
