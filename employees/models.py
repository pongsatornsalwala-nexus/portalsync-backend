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
    STATUS_IMPORTED = 'IMPORTED'
    STATUS_PENDING = 'PENDING'
    STATUS_REGISTERED = 'REGISTERED'
    STATUS_CHOICES = [
        (STATUS_IMPORTED, 'Imported'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_REGISTERED, 'Registered')
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
    prefix = models.CharField(
    max_length = 10,
    blank = True,
    null = True,
    choices = [
        ('mr', 'Mr.'),
        ('mrs', 'Mrs.'),
        ('ms', 'Ms.'),
    ],
    help_text = "Title prefix for AIA enrollment"
    )
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
    has_ssf = models.BooleanField(default=False, help_text="Enrolled in Social Security")
    has_aia = models.BooleanField(default=False, help_text="Enrolled in AIA Group")
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_CHOICES, default=REGISTER_IN)
    is_exiting_ssf = models.BooleanField(
        default=False,
        help_text="True if employee is currently exiting from SSF benefit"
    )
    is_exiting_aia = models.BooleanField(
        default=False,
        help_text="True if employee is currently exiting from AIA benefit"
    )

    ssf_activated = models.BooleanField(
        default=False,
        help_text="True if SSF registration has been officially confirmed and activated"
    )

    aia_activated = models.BooleanField(
        default=False,
        help_text="True if AIA registration has been officially confirmed and activated"
    )

    ssf_archived = models.BooleanField(
        default=False,
        help_text="True if SSF exit has been officially confirmed and archived"
    )

    aia_archived = models.BooleanField(
        default=False,
        help_text="True if AIA exit has been officially confirmed and archived"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_IMPORTED)
    ssf_status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True, help_text="SSF registration status (null if not enrolled)")
    aia_status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True, help_text="AIA registration status (null if not enrolled)")
    
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

    # AIA-specific Fields

    passport = models.CharField(
        max_length = 20,
        blank = True,
        null = True,
        help_text = "Passport number for non-Thai nationals"
    )

    designation = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        help_text = "Job title/position (AIA)"
    )


    # AIA Document Uploads
    national_id_file = models.FileField(
        upload_to='employee_documents/national_ids/',
        blank=True,
        null=True,
        help_text="National ID card scan/photo"
    )

    bank_book_file = models.FileField(
        upload_to='employee_documents/bank_books/',
        blank=True,
        null=True,
        help_text="Bank book cover page"
    )

    ceb_form_file = models.FileField(
        upload_to='employee_documents/ceb_forms/',
        blank=True,
        null=True,
        help_text="AIA CEB enrollment form"
    )

    def save(self, *args, **kwargs):
        """
        Override save to automatically set status fields based on enrollment.
        - Respects status passed in from Excel (only defaults if None)
        - Auto-computes general status as the least advanced of SSF/AIA
        """
        # Auto-initialize SSF status only if not already set
        if self.has_ssf and self.ssf_status is None:
            self.ssf_status = self.STATUS_IMPORTED
        elif not self.has_ssf:
            self.ssf_status = None

        # Auto-initialize AIA status only if not already set
        if self.has_aia and self.aia_status is None:
            self.aia_status = self.STATUS_IMPORTED
        elif not self.has_aia:
            self.aia_status = None

        # Auto-archive logic updated to use REGISTERED
        if self.is_exiting_ssf and self.ssf_status == self.STATUS_REGISTERED and not self.has_ssf:
            self.ssf_archived = True
        if self.is_exiting_aia and self.aia_status == self.STATUS_REGISTERED and not self.has_aia:
            self.aia_archived = True

        # Auto-compute general status as least advanced of SSF/AIA
        stage_order = [
            self.STATUS_IMPORTED,
            self.STATUS_PENDING,
            self.STATUS_REGISTERED
        ]
        active_statuses = [s for s in [self.ssf_status, self.aia_status] if s is not None]
        if active_statuses:
            # Find the one with the lowest index in stage_order
            self.status = min(active_statuses, key=lambda s: stage_order.index(s) if s in stage_order else 0)
        else:
            self.status = self.STATUS_IMPORTED # fallback

        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_card']),
            models.Index(fields=['worksite', 'has_ssf', 'has_aia']),
            models.Index(fields=['status']),
        ]
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id_card})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"