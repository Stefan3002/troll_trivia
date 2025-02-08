from django.urls import path

from trivia import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('play', views.Play.as_view(), name='play')
]