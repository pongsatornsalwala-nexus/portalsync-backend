from django.contrib import admin
# Import the models I want to register
# The `.` means "from the current app (benefits)""
from .models import Hospital, BenefitQueue

# Register your models here.

# Decorator (putting a label on a function)
# Tells Django "use this class to configure the Hospital admin page"
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    # Which columns to show in the list view
    list_display = ['name', 'province', 'hospital_type']
    # Add filter sidebar (filter by province/type)
    list_filter = ['province', 'hospital_type']
    # Add search box
    search_fields = ['name', 'province']
    # Default sort order
    ordering = ['province', 'name']