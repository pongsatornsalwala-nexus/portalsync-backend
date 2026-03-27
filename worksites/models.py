from django.db import models

SCHEDULE_CHOICES = [
    ('1st', 'Next Month 1st'),
    ('16th', 'Next Month 16th'),
    ('custom', 'Custom Date'),
]

class Worksite(models.Model):
    """
    Represents a worksite/location where employees work.
    Each worksite has independent sync policies for SSF and AIA.
    """
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default='fa-building')  # FontAwesome icon class
    color = models.CharField(max_length=20, default='blue')  # Tailwind color
    sync_ssf = models.BooleanField(default=True, help_text="Enable SSF sync for this worksite")
    sync_aia = models.BooleanField(default=True, help_text="Enable AIA sync for this worksite")

    # SSF registration schedule
    ssf_registration_schedule = models.CharField(
        max_length=10, choices=SCHEDULE_CHOICES, default='1st'
    )
    ssf_custom_date = models.DateField(null=True, blank=True)
    ssf_resign_limit = models.IntegerField(default=15)

    # AIA registration schedule
    aia_registration_schedule = models.CharField(
        max_length=10, choices=SCHEDULE_CHOICES, default='1st'
    )
    aia_custom_date = models.DateField(null=True, blank=True)
    aia_resign_limit = models.IntegerField(default=15)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name