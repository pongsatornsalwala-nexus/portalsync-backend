from django.db import models


class Worksite(models.Model):
    """
    Represents a worksite/location where employees work.
    Each worksite has different sync policies for SSF and AIA.
    """
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default='fa-building')  # FontAwesome icon class
    color = models.CharField(max_length=20, default='blue')  # Tailwind color
    hire_limit = models.IntegerField(default=30, help_text="Days within which to register new hires")
    resign_limit = models.IntegerField(default=15, help_text="Days within which to process resignations")
    sync_ssf = models.BooleanField(default=True, help_text="Enable SSF sync for this worksite")
    sync_aia = models.BooleanField(default=True, help_text="Enable AIA sync for this worksite")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name