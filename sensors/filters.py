import django_filters
from .models import PressureSensor, PressureReading

class PressureSensorFilter(django_filters.FilterSet):
    class Meta:
        model = PressureSensor
        fields = {
            'label': ['exact', 'icontains'],
            'installation_date': ['exact', 'year__gt'],
            'latitude': ['exact', 'gt', 'lt'],
            'longitude': ['exact', 'gt', 'lt'],
        }

class PressureReadingFilter(django_filters.FilterSet):
    from_date = django_filters.DateTimeFilter(field_name="datetime", lookup_expr='gte')
    to_date = django_filters.DateTimeFilter(field_name="datetime", lookup_expr='lte')

    class Meta:
        model = PressureReading
        fields = {
            'sensor': ['exact'],
            'datetime': ['exact', 'range'],
            'value': ['exact', 'gt', 'lt'],
        }
