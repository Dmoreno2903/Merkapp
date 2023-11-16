
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('main/', views.main, name='main'),
    path('logout/', views.signout, name='logout'),
    path('login/', views.signin, name='signin'),
    path('registros/', views.registros, name='registros'),
    path('supermercados/', views.supermercados, name='supermercados'),
]