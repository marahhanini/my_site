from django.urls import path,include
#from . import views
from rest_framework.routers import DefaultRouter
from .views import PressureSensorViewSet, PressureReadingViewSet
from django_filters.rest_framework import DjangoFilterBackend

router = DefaultRouter()
router.register(r'pressure_sensors', PressureSensorViewSet)
router.register(r'pressure_readings', PressureReadingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]