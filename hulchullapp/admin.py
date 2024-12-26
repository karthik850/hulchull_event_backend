from django.contrib import admin

from .models import SecretCodeDB

@admin.register(SecretCodeDB)
class SecretCodeDBAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'fav_number', 'associate_name', 'is_opened', 'opened_on')
    list_filter = ('is_opened',)
    search_fields = ('user_name', 'associate_name')

