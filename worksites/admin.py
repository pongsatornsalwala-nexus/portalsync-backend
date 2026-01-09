from django.contrib import admin
from .models import Worksite

@admin.register(Worksite)
class WorksiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color', 'hire_limit', 'resign_limit', 'sync_ssf', 'sync_aia']
    list_filter = ['sync_ssf', 'sync_aia']
    search_fields = ['name']