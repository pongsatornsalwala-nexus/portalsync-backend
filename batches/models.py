from django.db import models
from worksites.models import Worksite
from employees.models import Employee

# Create your models here.

class RegistrationBatch(models.Model):

    BENEFIT_CHOICES = [
        ('SSF', 'Social Security Fund'),
        ('AIA', 'AIA Group Insurance'),
    ]

    TYPE_CHOICES = [
        ('REGISTER_IN', 'Entry'),
        ('REGISTER_OUT', 'Exit'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('SUBMITTED', 'Submitted'),
        ('CLOSED', 'Closed'),
    ]

    worksite = models.ForeignKey(
        Worksite,
        on_delete=models.PROTECT,
        related_name='batches'
    )
    benefit = models.CharField(max_length=10, choices=BENEFIT_CHOICES)
    batch_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    registration_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    employees = models.ManyToManyField(
        Employee,
        related_name='batches',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # Prevent duplicate open batches for same worksite+benefit+type
        constraints = [
            models.UniqueConstraint(
                fields=['worksite', 'benefit', 'batch_type'],
                condition=models.Q(status='OPEN'),
                name='unique_open_batch_per_worksite_benefit_type'
            )
        ]
    
    def __str__(self):
        return f"{self.worksite.name} - {self.benefit} {self.batch_type} ({self.registration_date})"