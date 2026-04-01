from django.contrib import admin
from .models import RegistrationBatch

# Register your models here.

@admin.register(RegistrationBatch)
class RegistrationBatchAdmin(admin.ModelAdmin):
    list_display = ['worksite', 'benefit', 'batch_type', 'registration_date', 'status', 'created_at']
    list_filter = ['benefit', 'batch_type', 'status', 'worksite']