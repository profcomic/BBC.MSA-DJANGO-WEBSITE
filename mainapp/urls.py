from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('leadership/', views.leadership, name='leadership'),
    path('ministries/', views.ministries, name='ministries'),
    path('sermons/', views.sermons, name='sermons'),
    path('blog/', views.blog, name='blog'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
    path('berean-times-magazine/', views.berean_times_magazine, name='berean_times_magazine'),
    path('give/', views.give, name='give'),
]
