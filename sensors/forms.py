from django import forms
from django.core.exceptions import ValidationError
from .models import PressureSensor, PressureReading
from jsonschema import validate, ValidationError as JSONSchemaValidationError
from .constants import CONFIGURATION_SCHEMA


class PressureSensorForm(forms.ModelForm):
    class Meta:
        model = PressureSensor
        fields = '__all__'

    def clean_label(self):
        label = self.cleaned_data.get('label')
        if not label.startswith('PSSR'):
            raise ValidationError("Label must start with the prefix 'PSSR'.")
        return label
    
    def clean_configuration(self):
        configuration = self.cleaned_data.get('configuration')
        try:
            validate(instance=configuration, schema=CONFIGURATION_SCHEMA)
        except JSONSchemaValidationError as e:
            raise ValidationError(f"Invalid configuration: {e.message}")
        return configuration

class PressureReadingForm(forms.ModelForm):
    class Meta:
        model = PressureReading
        fields = '__all__'
