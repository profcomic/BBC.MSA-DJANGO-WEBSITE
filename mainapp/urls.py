from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sermons/', views.sermons, name='sermons'),
    path('events/', views.events, name='events'),
    path('contacts/', views.contacts, name='contacts'),
]
