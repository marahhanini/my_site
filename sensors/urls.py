from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AggregatePressureReadingsView, PressureSensorViewSet, PressureReadingViewSet, greeting

router = DefaultRouter()
router.register(r'sensors', PressureSensorViewSet)
router.register(r'readings', PressureReadingViewSet)

urlpatterns = [
    path('aggregate/', AggregatePressureReadingsView.as_view(), name='aggregate-pressure-readings'),
    path('greeting/', greeting, name='greeting'),
    path('', include(router.urls)),
]
