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
            'sync_ssf',
            'sync_aia',
            'ssf_registration_schedule',
            'ssf_custom_date',
            'ssf_resign_limit',
            'aia_registration_schedule',
            'aia_custom_date',
            'aia_resign_limit',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']