import uuid
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin

from my_tags.models import TaggedItem
from .forms import PressureReadingForm, PressureSensorForm
from .models import PressureReading, PressureSensor

class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 1

class BaseTaggedItemAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]

    def save_tags(self, obj, form):
        # Clear existing tags
        TaggedItem.objects.filter(content_type__model=obj._meta.model_name, object_id=obj.id).delete()
        # Save new tags
        tags = form.cleaned_data.get('tags', [])
        for tag in tags:
            TaggedItem.objects.create(tag=tag, content_object=obj)

@admin.register(PressureSensor)
class PressureSensorAdmin(BaseTaggedItemAdmin):
    form = PressureSensorForm
    list_display = ('label', 'installation_date', 'latitude', 'longitude', 'serial_number')
    search_fields = ('label',)
    readonly_fields = ('serial_number',)

    def save_model(self, request, obj, form, change):
        if not obj.serial_number:
            obj.serial_number = uuid.uuid4()
        obj.full_clean()
        super().save_model(request, obj, form, change)
        self.save_tags(obj, form)

@admin.register(PressureReading)
class PressureReadingAdmin(BaseTaggedItemAdmin):
    form = PressureReadingForm
    list_display = ('sensor', 'datetime', 'value')
    list_filter = ('sensor', 'datetime')
    search_fields = ('sensor__label',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        self.save_tags(obj, form)