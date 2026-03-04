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

    is_full = serializers.SerializerMethodField()

    def get_is_full(self, obj):
        # hasattr check because not every hospital has a status row yet
        if hasattr(obj, 'status'):
            return obj.status.is_full
        return False # default: not full

    # `model` - Which model to serialize
    # `fields` - Which fields to include in the JSON
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'province', 'hospital_type', 'is_full']