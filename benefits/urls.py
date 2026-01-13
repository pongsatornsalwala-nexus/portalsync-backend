from django.urls import path
from . import views

urlpatterns = [
    path('hospitals/', views.hospital_list, name = 'hospital-list'),
]