"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from employees.views import EmployeeViewSet
from worksites.views import WorksiteViewSet
from benefits.views import HospitalViewSet

# Create a router and register the viewsets
router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename = 'employee')
router.register(r'worksites', WorksiteViewSet, basename = 'worksite')
router.register(r'hospitals', HospitalViewSet, basename = 'hospital')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/benefits/', include('benefits.urls')),
    # path('api/', include(router.urls)), # All API endpoints will be under /api/
]