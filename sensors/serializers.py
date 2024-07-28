from rest_framework import serializers
from .models import PressureSensor, PressureReading
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError

class PressureSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PressureSensor
        fields = '__all__'

class PressureReadingSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", input_formats=["%Y-%m-%dT%H:%M:%S.%fZ"])

    class Meta:
        model = PressureReading
        fields = '__all__'

    def to_representation(self, instance):
       # Convert datetime to ISO format 
        representation = super().to_representation(instance)
        representation['datetime'] = instance.datetime.isoformat()
        return representation

    def to_internal_value(self, data):
        # Parse datetime from ISO format 
        if 'datetime' in data:
            data['datetime'] = parse_datetime(data['datetime'])
        return super().to_internal_value(data)
