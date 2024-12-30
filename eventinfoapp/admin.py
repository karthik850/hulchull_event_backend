from django.contrib import admin
from .models import Highlights,Events,ImportantPersons, Teams
# Register your models here.
@admin.register(Highlights)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image_url')
    search_fields = ('name', 'description')

@admin.register(Events)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(ImportantPersons)
class ImportantPersonsAdmin(admin.ModelAdmin):
    pass

@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    pass
