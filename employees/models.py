from django.db import models
from worksites.models import Worksite


class Employee(models.Model):
    """
    Represents an employee in the HR system.
    Tracks their personal information, employment details, and benefit enrollment.
    """
    
    # Benefit Type Choices
    BENEFIT_SSF = 'SSF'
    BENEFIT_AIA = 'AIA'
    BENEFIT_CHOICES = [
        (BENEFIT_SSF, 'Social Security Fund'),
        (BENEFIT_AIA, 'AIA Group Insurance'),
    ]
    
    # Registration Type Choices
    REGISTER_IN = 'REGISTER_IN'
    REGISTER_OUT = 'REGISTER_OUT'
    REGISTRATION_CHOICES = [
        (REGISTER_IN, 'Register In'),
        (REGISTER_OUT, 'Register Out'),
    ]
    
    # Status Choices
    STATUS_ENTRY = 'ENTRY'
    STATUS_PENDING = 'PENDING'
    STATUS_REVIEWING = 'REVIEWING'
    STATUS_REPORTED = 'REPORTED'
    STATUS_VERIFIED = 'VERIFIED'
    STATUS_CHOICES = [
        (STATUS_ENTRY, 'Entry'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_REVIEWING, 'Reviewing'),
        (STATUS_REPORTED, 'Reported'),
        (STATUS_VERIFIED, 'Verified'),
    ]
    
    # Gender Choices
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    ]
    
    # Personal Information
    id_card = models.CharField(max_length=17, unique=True, help_text="13-digit Thai ID in X-XXXX-XXXXX-XX-X format")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=GENDER_MALE)
    nationality = models.CharField(max_length=50, default='Thai')
    
    # Bank Information
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account = models.CharField(max_length=50, null=True, blank=True)
    
    # Employment Information
    employment_date = models.DateField()
    plan = models.CharField(max_length=50, blank=True, help_text="Insurance plan level")
    employee_no = models.CharField(max_length=50, blank=True, help_text="Company employee number")
    department = models.CharField(max_length=100, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Worksite & Benefits
    worksite = models.ForeignKey(Worksite, on_delete=models.PROTECT, related_name='employees')
    benefit_type = models.CharField(max_length=10, choices=BENEFIT_CHOICES, default=BENEFIT_SSF)
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_CHOICES, default=REGISTER_IN)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ENTRY)
    
    # Additional Fields
    effective_date = models.DateField(null=True, blank=True, help_text="Date when benefit becomes effective")
    resign_reason = models.TextField(blank=True, help_text="Reason for resignation (if REGISTER_OUT)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #SSF-specific Fields
    hospital_choice_1 = models.CharField(
        max_length = 200,
        blank = True,
        null = True,
        help_text = "Primary hospital choice for SSF"
    )

    hospital_choice_2 = models.CharField(
        max_length = 200,
        blank = True,
        null = True,
        help_text = "Secondary hospital choice for SSF"
    )

    hospital_choice_3 = models.CharField(
        max_length = 200,
        blank = True,
        null = True,
        help_text = "Tertiary hospital choice for SSF"
    )

    marital_status = models.CharField(
        max_length = 20,
        blank = True,
        null = True,
        choices = [
            ('single', 'Single'),
            ('married', 'Married'),
            ('widowed', 'Widowed'),
            ('divorced', 'Divorced'),
            ('separated', 'Separated'),
            ('other', 'Other'),
        ]
    )

    wage_type = models.CharField(
        max_length = 20,
        blank = True,
        null = True,
        choices = [
            ('daily', 'Daily'),
            ('monthly', 'Monthly')
        ]
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_card']),
            models.Index(fields=['worksite', 'benefit_type']),
            models.Index(fields=['status']),
        ]
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id_card})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"