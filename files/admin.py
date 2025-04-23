from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'size', 'uploaded_at', 'uploaded_by')
    list_filter = ('content_type', 'uploaded_at')
    search_fields = ('name', 'uploaded_by__username')
    readonly_fields = ('file_hash', 'uploaded_at')
    date_hierarchy = 'uploaded_at'

# Register your models here.
