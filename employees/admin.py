from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id_card', 'full_name', 'worksite', 'benefit_type', 'status', 'employment_date']
    list_filter = ['worksite', 'benefit_type', 'status', 'registration_type']
    search_fields = ['id_card', 'first_name', 'last_name']
    date_hierarchy = 'employment_date'

    fieldsets = (
        ('Personal Information', {
            'fields': ('id_card', 'first_name', 'last_name', 'date_of_birth', 'gender', 'nationality')
        }),
        ('Employment', {
            'fields': ('worksite', 'employment_date', 'employee_no', 'department', 'salary', 'plan')
        }),
        ('Benefits', {
            'fields': ('benefit_type', 'registration_type', 'status', 'effective_date')
        }),
        ('Banking', {
            'fields': ('bank_name', 'bank_account')
        }),
        ('Resignation', {
            'fields': ('resign_reason',),
            'classes': ('collapse',)
        }),
    )