from xml.dom.minidom import Document
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('problems/<str:pk>/', views.problemPage, name='problemPage'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('code/<str:pk>/', views.codePage, name='codePage'),
]
