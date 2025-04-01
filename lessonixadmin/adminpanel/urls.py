from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('classes/', views.classesPage, name='classes'),
    path('addclass/', views.addClassPage, name='addclass'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
