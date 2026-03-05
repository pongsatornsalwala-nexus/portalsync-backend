from django.shortcuts import render
from rest_framework import viewsets
# Imports
# `api_view` - Decorator that makes a function into an API endpoint
# `Response` - Returns JSON data to the frontend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Hospital, HospitalStatus
from .serializers import HospitalSerializer

# Create your views here.

class HospitalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Hospital model.
    Automatically provides list, create, retrieve, update, and destroy acitons.
    """
    queryset = Hospital.objects.select_related('status').all()
    serializer_class = HospitalSerializer

# The decorator
# Says "This view only accepts GET requests"
# Like saying "This is a read-only endpoint, no POST/PUT/DELETE"
@api_view(['GET'])
def hospital_list(request):
    hospitals = Hospital.objects.all()
    serializer = HospitalSerializer(hospitals, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def toggle_hospital_full(request, hospital_id):
    """
    Toggles the is_full status of a hospital.
    get_or_create means: find the HospitalStatus row, or make one if it doesn't exist yet.
    """
    try:
        hospital = Hospital.objects.get(id=hospital_id)
    except Hospital.DoesNotExist:
        return Response({'error': 'Hospital not found'}, status=status.HTTP_404_NOT_FOUND)

    hospital_status, created = HospitalStatus.objects.get_or_create(hospital=hospital)
    hospital_status.is_full = not hospital_status.is_full # flip it
    hospital_status.save()

    return Response({
        'id': hospital.id,
        'is_full': hospital_status.is_full
    })

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