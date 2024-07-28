from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Question, Choice
from my_tags.models import Tag, TaggedItem

class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 1

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date')
    inlines = [ChoiceInline, TaggedItemInline]
    fields = ('question_text', 'pub_date', 'tags')  # This line can be kept if 'tags' is a ManyToManyField in Question
    filter_horizontal = ('tags',)  # This line can be removed if 'tags' is not a ManyToManyField in Question
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        TaggedItem.objects.filter(content_type__model='question', object_id=obj.id).delete()
        for tag in form.cleaned_data.get('tags', []):
            TaggedItem.objects.create(tag=tag, content_object=obj)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'votes', 'display_tags')
    list_filter = ('question',)
    search_fields = ('choice_text',)
    inlines = [TaggedItemInline]  # Add this line to display TaggedItem inline

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    display_tags.short_description = 'Tags'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        TaggedItem.objects.filter(content_type__model='choice', object_id=obj.id).delete()
        for tag in form.cleaned_data.get('tags', []):
            TaggedItem.objects.create(tag=tag, content_object=obj)
