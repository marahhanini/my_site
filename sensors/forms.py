from django import forms
from django.core.exceptions import ValidationError
from .models import PressureSensor, PressureReading

class PressureSensorForm(forms.ModelForm):
    class Meta:
        model = PressureSensor
        fields = '__all__'

    def clean_label(self):
        label = self.cleaned_data.get('label')
        if not label.startswith('PSSR'):
            raise ValidationError("Label must start with the prefix 'PSSR'.")
        return label

class PressureReadingForm(forms.ModelForm):
    class Meta:
        model = PressureReading
        fields = '__all__'
