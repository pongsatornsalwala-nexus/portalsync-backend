from rest_framework import serializers
from .models import Hospital

# `ModelSerializer` is a shortcut provided by Django REST Framework
# It automatically creates a serializer based on the model
# No need to manually define each field
class HospitalSerializer(serializers.ModelSerializer):
    """
    Serializer for Hospital model.
    Converts Hospital objects to JSON and vice versa.
    """

    # `model` - Which model to serialize
    # `fields` - Which fields to include in the JSON
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'province', 'hospital_type']