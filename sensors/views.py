import logging
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Sum, Avg
from django.utils.dateparse import parse_datetime
from .models import PressureSensor, PressureReading
from .serializers import PressureSensorSerializer, PressureReadingSerializer
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
   
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
    
        return request.user and request.user.is_authenticated


class AggregatePressureReadingsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        since = request.GET.get('since')
        until = request.GET.get('until')
        calculation = request.GET.get('calculation')

        if not all([since, until, calculation]):
            return Response({'error': 'Missing query parameters'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            since_dt = parse_datetime(since)
            until_dt = parse_datetime(until)
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        if since_dt >= until_dt:
            return Response({'error': 'The until date must be after the since date'}, status=status.HTTP_400_BAD_REQUEST)

        if calculation not in ['sum', 'avg']:
            return Response({'error': 'Invalid calculation parameter'}, status=status.HTTP_400_BAD_REQUEST)

        readings = PressureReading.objects.filter(datetime__gte=since_dt, datetime__lte=until_dt)

        if calculation == 'sum':
            result = readings.aggregate(total=Sum('value'))['total'] or 0
        elif calculation == 'avg':
            result = readings.aggregate(average=Avg('value'))['average'] or 0

        return Response({'result': result})

class PressureSensorViewSet(viewsets.ModelViewSet):
    queryset = PressureSensor.objects.all()
    serializer_class = PressureSensorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PressureReadingViewSet(viewsets.ModelViewSet):
    queryset = PressureReading.objects.all()
    serializer_class = PressureReadingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@login_required(login_url='/admin/login/')
def greeting(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': f'Hello {request.user.username}!'})
    else:
        return JsonResponse({'message': 'Hello Guest!'})
