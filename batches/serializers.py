from rest_framework import serializers
from .models import RegistrationBatch
from employees.serializers import EmployeeListSerializer

class RegistrationBatchSerializer(serializers.ModelSerializer):
    employees_detail = EmployeeListSerializer(
        source='employees',
        many=True,
        read_only=True
    )
    worksite_name = serializers.CharField(source='worksite.name', read_only=True)
    employee_count = serializers.IntegerField(source='employees.count', read_only=True)

    class Meta:
        model = RegistrationBatch
        fields = [
            'id',
            'worksite',
            'worksite_name',
            'benefit',
            'batch_type',
            'registration_date',
            'status',
            'employee_count',
            'employees',
            'employees_detail',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']