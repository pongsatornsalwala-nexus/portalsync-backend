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
            'ssf_exit_schedule',
            'ssf_exit_custom_date',
            'aia_registration_schedule',
            'aia_custom_date',
            'aia_exit_schedule',
            'aia_exit_custom_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']