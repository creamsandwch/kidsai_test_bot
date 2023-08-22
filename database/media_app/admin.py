from django.contrib import admin

from .models import MediaIds


@admin.register(MediaIds)
class MediaIdsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'file_id',
        'filename'
    ]
