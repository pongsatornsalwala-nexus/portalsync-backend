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

    @action(detail=False, methods=['get'])
    def download_template(self, request):
        """
        GET /api/employees/download_template/
        Downloads the Excel template for batch upload
        """
        import os
        from django.http import FileResponse
        from django.conf import settings

        # Build the path to the template file
        template_path = os.path.join(
            settings.BASE_DIR,
            'templates',
            'SSF AIA Bulk Import Template.xlsx'
        )

        if not os.path.exists(template_path):
            return Response(
                {'error': 'Template file not found.'},
                status = status.HTTP_404_NOT_FOUND
            )

        # Open and return the file
        file = open(template_path, 'rb')
        response = FileResponse(
            file,
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment;  filename="SSF_AIA_Bulk_Import_Template.xlsx"'

        return response

    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        """
        POST /api/employees/bulk_upload/
        Uploads and processes Excel file to create employees in bulk
        """
        import openpyxl
        from datetime import datetime

        # Get the uploaded file
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response(
                {'error': 'No file uploaded'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get context data
        worksite_id = request.data.get('worksite_id')
        registration_type = request.data.get('registration_type')
        benefit_type = request.data.get('benefit_type')

        if not worksite_id:
            return Response(
                {'error': 'Worksite ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Load the Excel file
            wb = openpyxl.load_workbook(uploaded_file)
            ws = wb.active

            created_count = 0
            errors = []

            # Start reading from row 5 (skip header rows 1-4)
            for row_num in range(5, ws.max_row + 1):
                try:
                    # Read data from each column
                    full_name = ws[f'B{row_num}'].value # Name
                    national_id = ws[f'D{row_num}'].value # National ID
                    hospital1 = ws[f'E{row_num}'].value # Hospital Choice 1
                    hospital2 = ws[f'F{row_num}'].value # Hospital Choice 2
                    hospital3 = ws[f'G{row_num}'].value # Hospital Choice 3
                    dob = ws[f'H{row_num}'].value # Date of Birth (Buddhist Era)
                    employment_date = ws[f'I{row_num}'].value # Employment Date (Buddhist Era)

                    # Skip empty rows
                    if not full_name or not national_id:
                        continue

                    # Parse name: "นาย test test" -> prefix="mr", firstName="test", lastName="test"abs
                    prefix = None
                    first_name = None
                    last_name = None

                    if full_name:
                        name_parts = str(full_name).strip().split()
                        if len(name_parts) >= 3:
                            # Has prefix
                            prefix_thai = name_parts[0]
                            if prefix_thai == 'นาย':
                                prefix = 'mr'
                            elif prefix_thai == 'นาง':
                                prefix = 'mrs'
                            elif prefix_thai == 'นางสาว':
                                prefix = 'ms'

                            first_name = name_parts[1]
                            last_name = ' '.join(name_parts[2:])
                        elif len(name_parts) == 2:
                            # No prefix
                            first_name = name_parts[0]
                            last_name = name_parts[1]
                        else:
                            # Single name
                            first_name = name_parts[0]
                            last_name = ''
                    
                    # Determine gender from prefix
                    gender = 'male' if prefix == 'mr' else 'female'

                    # Parse date: "25/6/2547" -> convert Buddhist year to Gregorian
                    def parse_buddhist_date(date_str):
                        if not date_str:
                            return None
                        try:
                            # Handle different formats
                            if isinstance(date_str, str):
                                parts = date_str.split('/')
                                if len(parts) == 3:
                                    day = int(parts[0])
                                    month = int(parts[1])
                                    year = int(parts[2]) - 543 # Convert Buddhist to Gregorian
                                    return f'{year:04d}-{month:02d}-{day:02d}'
                            return None
                        except:
                            return None

                    date_of_birth = parse_buddhist_date(dob)
                    employment_date_parsed = parse_buddhist_date(employment_date)

                    # Create employee
                    employee_data = {
                        'id_card': str(national_id).replace('-', ''),
                        'prefix': prefix,
                        'first_name': first_name,
                        'last_name': last_name,
                        'date_of_birth': date_of_birth,
                        'gender': gender,
                        'nationality': 'thai',
                        'employment_date': employment_date_parsed or datetime.now().date(),
                        'worksite': int(worksite_id),
                        'has_ssf': benefit_type == 'SSF',
                        'has_aia': benefit_type == 'AIA',
                        'registration_type': registration_type,
                        'hospital_choice_1': hospital1,
                        'hospital_choice_2': hospital2,
                        'hospital_choice_3': hospital3,
                    }

                    # Create the employee
                    Employee.objects.create(**employee_data)
                    created_count += 1

                except Exception as e:
                    errors.append(f'Row {row_num}: {str(e)}')
                    continue

            return Response({
                'success': True,
                'created_count': created_count,
                'errors': errors if errors else None,
            })

        except Exception as e:
            return Response(
                {'error': f'Failed to process file: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )