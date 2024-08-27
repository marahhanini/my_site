from django.urls import path
from .views import AggregatePressureReadingsView, greeting

urlpatterns = [
    path('aggregate/', AggregatePressureReadingsView.as_view(), name='aggregate-pressure-readings'),
    path('greeting/', greeting, name='greeting'),
]
