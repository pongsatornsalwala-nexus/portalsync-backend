from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Worksite
from .serializers import WorksiteSerializer

class WorksiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Worksites.

    Provides CRUD operations:
    - GET /api/worksites/ : List all worksites
    - POST /api/worksites/ : Create new worksite
    - GET /api/worksites/{id}/ - Get specific worksite
    - PUT /api/worksites/{id}/ - Update worksite
    - DELETE /api/worksites/{id}/ - Delete worksite
    """
    queryset = Worksite.objects.all()
    serializer_class = WorksiteSerializer

    @action(detail = False, methods = ['get'])
    def count(self, request):
        """
        Custom endpoint: GET /api/worksites/count/
        Returns the total number of worksites.
        """
        count = self.queryset.count()
        return Response({'count': count})