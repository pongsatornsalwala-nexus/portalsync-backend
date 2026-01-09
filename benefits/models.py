from django.db import models
from employees.models import Employee


class BenefitQueue(models.Model):
    """
    Tracks the processing queue for SSF and AIA benefit registrations.
    Used in the Portal Sync page to show pipeline status.
    """
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='benefit_queues')
    
    # Hospital choices (for SSF only)
    hospital_choice_1 = models.CharField(max_length=200, blank=True)
    hospital_choice_2 = models.CharField(max_length=200, blank=True)
    hospital_choice_3 = models.CharField(max_length=200, blank=True)
    
    # Processing information
    processed_by = models.CharField(max_length=100, blank=True, help_text="Admin who processed this")
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Benefit Queues"
        
    def __str__(self):
        return f"{self.employee.full_name} - {self.employee.benefit_type} Queue"