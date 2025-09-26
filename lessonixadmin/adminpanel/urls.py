from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('classes/', views.classesPage, name='classes'),
    path('addclass/', views.addClassPage, name='addclass'),
    path('addstaff/<str:type>', views.addStaffPage, name='addstaff'),
    path('editstaff/<str:stringid>/', views.editStaffPage, name='editstaff'),
    path('staff/', views.staffPage, name='staff'),
    path('staff/<str:stringid>/', views.staffProfile, name='staffprofile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
