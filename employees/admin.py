from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id_card', 'full_name', 'worksite', 'has_ssf', 'has_aia', 'status', 'employment_date']
    list_filter = ['worksite', 'has_ssf', 'has_aia', 'status', 'registration_type']
    search_fields = ['id_card', 'first_name', 'last_name']
    date_hierarchy = 'employment_date'

    fieldsets = (
        ('Personal Information', {
            'fields': ('id_card', 'prefix', 'first_name', 'last_name', 'date_of_birth', 'gender', 'nationality', 'marital_status')
        }),
        ('Employment', {
            'fields': ('worksite', 'employment_date', 'employee_no', 'department', 'salary', 'plan', 'wage_type')
        }),
        ('Benefits', {
            'fields': ('has_ssf', 'has_aia', 'registration_type', 'status', 'effective_date')
        }),
        ('SSF Hospital Choices', {
            'fields': ('hospital_choice_1', 'hospital_choice_2', 'hospital_choice_3'),
            'classes': ('collapse',),
        }),
        ('AIA Information', {
            'fields': ('passport', 'designation'),
            'classes': ('collapse',),
        }),
        ('Banking', {
            'fields': ('bank_name', 'bank_account')
        }),
        ('Resignation', {
            'fields': ('resign_reason',),
            'classes': ('collapse',)
        }),
    )