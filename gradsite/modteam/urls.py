from django.urls import path
from . import views

app_name = 'modteam'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('about/', views.about, name='about'),
]
