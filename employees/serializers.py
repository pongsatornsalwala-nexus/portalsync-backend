from rest_framework import serializers
from .models import Employee
from worksites.serializers import WorksiteSerializer

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee model.
    Includes nested worksite information.
    """
    worksite_detail = WorksiteSerializer(source = 'worksite', read_only = True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'id_card',
            'first_name',
            'last_name',
            'full_name',
            'date_of_birth',
            'gender',
            'nationality',
            'bank_name',
            'bank_account',
            'employment_date',
            'plan',
            'employee_no',
            'department',
            'salary',
            'worksite',
            'worksite_detail',
            'benefit_type',
            'registration_type',
            'status',
            'effective_date',
            'resign_reason',
            'created_at',
            'updated_at',
            'hospital_choice_1',
            'hospital_choice_2',
            'hospital_choice_3',
            'marital_status',
            'wage_type',
            'prefix',
            'passport',
            'designation',
        ]
        read_only_fields = ['id', 'full_name', 'created_at', 'updated_at']

class EmployeeListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing employees (without full details).
    """
    worksite_name = serializers.CharField(source = 'worksite.name', read_only = True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'id_card',
            'first_name',
            'last_name',
            'full_name',
            'date_of_birth',
            'gender',
            'nationality',
            'marital_status',
            'bank_name',
            'bank_account',
            'passport',
            'prefix',
            'worksite',
            'worksite_name',
            'benefit_type',
            'status',
            'employment_date',
            'department',
            'hospital_choice_1',
        ]