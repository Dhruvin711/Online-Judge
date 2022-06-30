from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('problems/<str:pk>/', views.problemPage, name='problemPage'),
]
