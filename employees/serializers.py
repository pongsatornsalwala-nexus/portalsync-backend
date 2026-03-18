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
            'prefix',
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
            'has_ssf',
            'has_aia',
            'registration_type',
            'status',
            'ssf_status',
            'aia_status',
            'is_exiting_ssf',
            'is_exiting_aia',
            'ssf_exit_status',
            'aia_exit_status',
            'ssf_activated',
            'aia_activated',
            'ssf_archived',
            'aia_archived',
            'effective_date',
            'resign_reason',
            'created_at',
            'updated_at',
            'hospital_choice_1',
            'hospital_choice_2',
            'hospital_choice_3',
            'marital_status',
            'wage_type',
            'ssf_type',
            'passport',
            'designation',
            'national_id_file',
            'bank_book_file',
            'ceb_form_file',
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
            'prefix',
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
            'designation',
            'national_id_file',
            'bank_book_file',
            'ceb_form_file',
            'worksite',
            'worksite_name',
            'has_ssf',
            'has_aia',
            'registration_type',
            'status',
            'ssf_status',
            'aia_status',
            'is_exiting_ssf',
            'is_exiting_aia',
            'ssf_exit_status',
            'aia_exit_status',
            'ssf_activated',
            'aia_activated',
            'ssf_archived',
            'aia_archived',
            'employment_date',
            'plan',
            'employee_no',
            'department',
            'salary',
            'effective_date',
            'resign_reason',
            'created_at',
            'hospital_choice_1',
            'hospital_choice_2',
            'hospital_choice_3',
            'wage_type',
            'ssf_type',
        ]