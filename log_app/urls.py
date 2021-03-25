from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('register', views.registration),
    path('login', views.login),
    path('success', views.success_page),
    path('logout', views.logout),
]