from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from .models import PressureSensor, PressureReading
from .serializers import PressureSensorSerializer, PressureReadingSerializer
from .filters import PressureSensorFilter, PressureReadingFilter
from django.utils.dateparse import parse_datetime

class PressureSensorViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = PressureSensor.objects.all()
    serializer_class = PressureSensorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PressureSensorFilter

class PressureReadingViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = PressureReading.objects.all()
    serializer_class = PressureReadingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PressureReadingFilter

  