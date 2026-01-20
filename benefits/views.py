from django.shortcuts import render
from rest_framework import viewsets
# Imports
# `api_view` - Decorator that makes a function into an API endpoint
# `Response` - Returns JSON data to the frontend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Hospital
from .serializers import HospitalSerializer

# Create your views here.

class HospitalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Hospital model.
    Automatically provides list, create, retrieve, update, and destroy acitons.
    """
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

# The decorator
# Says "This view only accepts GET requests"
# Like saying "This is a read-only endpoint, no POST/PUT/DELETE"
@api_view(['GET'])

# The function
def hospital_list(request):
    """
    API endpoint to get all hospitals.
    Returns list of hospitals with id, name, province, and type.
    """
    hospitals = Hospital.objects.all()
    serializer = HospitalSerializer(hospitals, many = True)
    return Response(serializer.data)

# Serializer is a translator between Python objects and JSON