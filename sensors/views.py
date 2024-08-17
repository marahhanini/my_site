from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Sum, Avg
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from .models import PressureSensor, PressureReading
from .serializers import PressureSensorSerializer, PressureReadingSerializer

@require_http_methods(["GET"])
def aggregate_pressure_readings(request):
    since = request.GET.get('since')
    until = request.GET.get('until')
    calculation = request.GET.get('calculation')

    if not all([since, until, calculation]):
        return JsonResponse({'error': 'Missing query parameters'}, status=400)

    try:
        since_dt = parse_datetime(since)
        until_dt = parse_datetime(until)
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    if calculation not in ['sum', 'avg']:
        return JsonResponse({'error': 'Invalid calculation parameter'}, status=400)

    readings = PressureReading.objects.filter(datetime__gte=since_dt, datetime__lte=until_dt)

    if calculation == 'sum':
        result = readings.aggregate(total=Sum('value'))['total']
    elif calculation == 'avg':
        result = readings.aggregate(average=Avg('value'))['average']

    return JsonResponse({'result': result})

class AggregatePressureReadingsView(APIView):
    def get(self, request):
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

        if calculation not in ['sum', 'avg']:
            return Response({'error': 'Invalid calculation parameter'}, status=status.HTTP_400_BAD_REQUEST)

        readings = PressureReading.objects.filter(datetime__gte=since_dt, datetime__lte=until_dt)

        if calculation == 'sum':
            result = readings.aggregate(total=Sum('value'))['total']
        elif calculation == 'avg':
            result = readings.aggregate(average=Avg('value'))['average']

        return Response({'result': result})

class PressureSensorViewSet(viewsets.ModelViewSet):
    queryset = PressureSensor.objects.all()
    serializer_class = PressureSensorSerializer

class PressureReadingViewSet(viewsets.ModelViewSet):
    queryset = PressureReading.objects.all()
    serializer_class = PressureReadingSerializer
