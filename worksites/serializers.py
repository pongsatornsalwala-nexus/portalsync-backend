from rest_framework import serializers
from .models import Worksite

class WorksiteSerializer(serializers.ModelSerializer):
    """
    Seriailizer for the Worksite model.
    Converts Worksite objects to/from JSON for the API.
    """
    
    class Meta:
        model = Worksite
        fields = [
            'id',
            'name',
            'icon',
            'color',
            'hire_limit',
            'resign_limit',
            'sync_ssf',
            'sync_aia',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']