from django.db import models
from django.core.exceptions import ValidationError
from my_tags.models import Tag
from django.utils import timezone
import uuid

def generate_serial_number():
    return str(uuid.uuid4())

class PressureSensor(models.Model):
    label = models.CharField(max_length=100)
    installation_date = models.DateTimeField(default=timezone.now)
    latitude = models.FloatField()
    longitude = models.FloatField()
    serial_number = models.CharField(max_length=100, unique=True,null=True,default=generate_serial_number,editable=False)
    tags = models.ManyToManyField(Tag, blank=True)
    
    def clean(self):
        super().clean()  
        if not self.label.startswith('PSSR'):
            raise ValidationError({'label': 'Label must start with the prefix "PSSR".'})
        
    def __str__(self):
        return self.label

class PressureReading(models.Model):
    sensor = models.ForeignKey(PressureSensor, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    value = models.FloatField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.sensor.label} - {self.datetime} - {self.value}'
