from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PressureSensorViewSet, PressureReadingViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .views import aggregate_pressure_readings, AggregatePressureReadingsView


router = DefaultRouter()
router.register(r'pressure_sensors', PressureSensorViewSet)
router.register(r'pressure_readings', PressureReadingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('aggregate/fbv/', aggregate_pressure_readings, name='aggregate_fbv'),
    path('aggregate/cbv/', AggregatePressureReadingsView.as_view(), name='aggregate_cbv'),
]