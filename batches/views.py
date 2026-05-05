from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import RegistrationBatch
from .serializers import RegistrationBatchSerializer
from employees.models import Employee
from worksites.models import Worksite
import datetime

# Create your views here.

def calculate_registration_date(worksite, benefit, batch_type):
    """
    Mirror of the frontend calculateRegistrationDate() logic.
    Returns a date object based on the worksite's schedule settings.
    """
    today = datetime.date.today()

    if batch_type == 'REGISTER_IN':
        schedule = worksite.ssf_registration_schedule if benefit == 'SSF' else worksite.aia_registration_schedule
        custom_day = worksite.ssf_custom_date if benefit == 'SSF' else worksite.aia_custom_date
    else:
        schedule = worksite.ssf_exit_schedule if benefit == 'SSF' else worksite.aia_exit_schedule
        custom_date = worksite.ssf_exit_custom_date if benefit == 'SSF' else worksite.aia_exit_custom_date

    if schedule == 'today':
        return today
    if schedule == 'custom' and custom_date:
        return custom_date
    if schedule == '1st':
        # Next month's 1st
        if today.month == 12:
            return datetime.date(today.year + 1, 1, 1)
        return datetime.date(today.year, today.month + 1, 1)
    if schedule == '16th':
        if today.day < 16:
            return datetime.date(today.year, today.month, 16)
        # Next month's 16th
        if today.month == 12:
            return datetime.date(today.year + 1, 1, 16)
        return datetime.date(today.year, today.month + 1, 16)

    return today # fallback

class RegistrationBatchViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationBatchSerializer 

    def get_queryset(self):
        queryset = RegistrationBatch.objects.prefetch_related('employees').select_related('worksite').all()

        worksite_id = self.request.query_params.get('worksite')
        benefit = self.request.query_params.get('benefit')
        batch_type = self.request.query_params.get('batch_type')
        status_filter = self.request.query_params.get('status')

        if worksite_id:
            queryset = queryset.filter(worksite_id=worksite_id)
        if benefit:
            queryset = queryset.filter(benefit=benefit)
        if batch_type:
            queryset = queryset.filter(batch_type=batch_type)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @action(detail=False, methods=['post'])
    def get_or_create_open(self, request):
        """
        POST /api/batches/get_or_create_open/
        Body: { worksite: 1, benefit: "SSF", batch_type: "REGISTER_IN" }

        Finds the existing OPEN batch for this combo, or creates one.
        Also syncs employees into the batch automatically.
        """
        worksite_id = request.data.get('worksite')
        benefit = request.data.get('benefit')
        batch_type = request.data.get('batch_type')

        if not all([worksite_id, benefit, batch_type]):
            return Response(
                {'error': 'worksite, benefit, and batch_type are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            worksite = Worksite.objects.get(id=worksite_id)
        except Worksite.DoesNotExist:
            return Response({'error': 'Worksite not found'}, status=status.HTTP_404_NOT_FOUND)

        # Calculate the registration date from worksite schedule
        reg_date = calculate_registration_date(worksite, benefit, batch_type)

        # Get or create the open batch
        batch, created = RegistrationBatch.objects.get_or_create(
            worksite=worksite,
            benefit=benefit,
            batch_type=batch_type,
            status='OPEN',
            defaults={'registration_date': reg_date}
        )

        # Auto-sync employees into the batch
        if benefit == 'SSF':
            if batch_type == 'REGISTER_IN':
                employees = Employee.objects.filter(
                    worksite=worksite,
                    has_ssf=True,
                    ssf_activated=False,
                    is_exiting_ssf=False,
                )
            else:
                employees = Employee.objects.filter(
                    worksite=worksite,
                    is_exiting_ssf=True,
                    ssf_archived=False,
                )
        else: # AIA
            if batch_type == 'REGISTER_IN':
                employees = Employee.objects.filter(
                    worksite=worksite,
                    has_aia=True,
                    aia_activated=False,
                    is_exiting_aia=False,
                )
            else:
                employees = Employee.objects.filter(
                    worksite=worksite,
                    is_exiting_aia=True,
                    aia_archived=False,
                )

        # Set (replace) the employees in this batch
        batch.employees.set(employees)

        serializer = self.get_serializer(batch)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        POST /api/batches/{id}/submit/
        Stamps effective_date on all employees in the batch,
        then marks the batch as SUBMITTED.
        Wrapped in a transaction so it's all-or-nothing.
        """
        batch = self.get_object()

        if batch.status != 'OPEN':
            return Response(
                {'error': f'Batch is already {batch.status} and cannot be submitted again'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                # Stamp effective_date on every employee in the batch
                batch.employees.all().update(
                    effective_date=batch.registration_date
                )

                # Auto-activate (entry) or auto-archive (exit)
                if batch.batch_type == 'REGISTER_IN':
                    if batch.benefit == 'SSF':
                        batch.employees.all().update(ssf_activated=True)
                    else:
                        batch.employees.all().update(aia_activated=True)
                else: # REGISTER_OUT
                    if batch.benefit == 'SSF':
                        batch.employees.all().update(ssf_archived=True)
                    else:
                        batch.employees.all().update(aia_archived=True)

                # Mark batch as SUBMITTED
                batch.status = 'SUBMITTED'
                batch.save()

        except Exception as e:
            return Response(
                {'error': f'Failed to submit batch: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = self.get_serializer(batch)
        return Response(serializer.data)