from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('popular/', views.popular, name='popular'),
    path('latest/', views.latest, name='latest'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
]
