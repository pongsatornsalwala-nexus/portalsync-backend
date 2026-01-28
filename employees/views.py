from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeListSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Employees

    Provides CRUD operations plus custom endpoints for dashboard stats.
    """
    queryset = Employee.objects.select_related('worksite').all()

    def get_serializer_class(self):
        """Use simplified serializer for list view, full serializer for detail view."""
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeSerializer

    @action(detail = False, methods = ['get'])
    def count(self, request):
        """
        GET /api/employees/count/
        Returns total count of employees.
        """
        count = self.queryset.count()
        return Response({'count': count})
    
    @action(detail = False, methods = ['get'])
    def stats(self, request):
        """
        GET /api/employees/stats/
        Returns dashboard statistics:
        - Total employees
        - New joiners (this month)
        - Resignations (this month)
        - Pending actions
        - SSF queue counts
        - AIA queue counts
        """
        from django.utils.timezone import now
        from datetime import timedelta

        # Get date range for "this month"
        today = now()
        month_start = today.replace(day = 1)

        total = self.queryset.count()

        # New joiners this month
        new_joiners = self.queryset.filter(
            employment_date__gte = month_start,
            registration_type = 'REGISTER_IN'
        ).count()

        # Resignations this month
        resignations = self.queryset.filter(
            updated_at__gte = month_start,
            registration_type = 'REGISTER_OUT'
        ).count()

        # Pending actions (not yet verified)
        pending = self.queryset.exclude(status = 'VERIFIED').count()

        # SSF queue counts
        ssf_register_in = self.queryset.filter(
            has_ssf = True,
            registration_type = 'REGISTER_IN',
            status__in = ['ENTRY', 'PENDING', 'REVIEWING']
        ).count()

        ssf_register_out = self.queryset.filter(
            has_ssf = True,
            registration_type = 'REGISTER_OUT',
            status__in = ['ENTRY', 'PENDING', 'REVIEWING']
        ).count()

        # AIA queue counts
        aia_register_in = self.queryset.filter(
            has_aia = True,
            registration_type = 'REGISTER_IN',
            status__in = ['ENTRY', 'PENDING', 'REVIEWING']
        ).count()

        aia_register_out = self.queryset.filter(
            has_aia = True,
            registration_type = 'REGISTER_OUT',
            status__in = ['ENTRY', 'PENDING', 'REVIEWING']
        ).count()

        return Response({
            'total_employees': total,
            'new_joiners': new_joiners,
            'resignations': resignations,
            'pending_actions': pending,
            'ssf_queue': {
                'register_in': ssf_register_in,
                'register_out': ssf_register_out,
            },
            'aia_queue': {
                'register_in': aia_register_in,
                'register_out': aia_register_out,
            }
        })
    
    @action(detail = False, methods = ['get'])
    def by_worksite(self, request):
        """
        GET /api/employees/by_worksite/?worksite_id = 1
        Returns employees filtered by worksite.
        """
        worksite_id = request.query_params.get('worksite_id')
        if worksite_id:
            employees = self.queryset.filter(worksite_id = worksite_id)
        else:
            employees = self.queryset.all()

        serializer = self.get_serializer(employees, many = True)
        return Response(serializer.data)