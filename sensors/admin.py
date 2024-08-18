# sensors/admin.py
import uuid

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from my_tags.models import TaggedItem

from .forms import PressureReadingForm, PressureSensorForm
from .models import PressureReading, PressureSensor


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 1

@admin.register(PressureSensor)
class PressureSensorAdmin(admin.ModelAdmin):
    form = PressureSensorForm
    list_display = ('label', 'installation_date', 'latitude', 'longitude', 'serial_number')
    search_fields = ('label',)
    readonly_fields = ('serial_number',) 
    inlines = [TaggedItemInline]
    
    def save_model (self ,request ,obj ,form ,change):
        if not obj.serial_number:
            obj.serial_number = uuid.uuid4()
        obj.full_clean()
        super().save_model(request,obj,form,change)
        # Handle save tags
        TaggedItem.objects.filter(content_type__model='pressuresensor',object_id=obj.id).delete()
        for tag in form.cleaned_data.get('tags', []):
            TaggedItem.objects.create(tag=tag, content_object=obj)

@admin.register(PressureReading)
class PressureReadingAdmin(admin.ModelAdmin):
    form = PressureReadingForm
    list_display = ('sensor', 'datetime', 'value')
    list_filter = ('sensor', 'datetime')
    search_fields = ('sensor__label',)
    inlines = [TaggedItemInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Handle save tags
        TaggedItem.objects.filter(content_type__model='pressurereading',object_id=obj.id).delete()
        for tag in form.cleaned_data.get('tags', []):
            TaggedItem.objects.create(tag=tag, content_object=obj)
