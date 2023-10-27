from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('signup', views.signup,name="signup"),
    path('signin', views.signin,name="signin"),
    path('signout', views.signout,name="signout"),
    path('first', views.first,name="first"),
    path('doctors', views.Doctors, name='doctors'),
    path('department', views.department, name='department'),
    path('booking', views.booking, name='booking'),
    
]
 