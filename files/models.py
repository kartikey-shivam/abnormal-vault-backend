from django.db import models
from django.contrib.auth.models import User
import hashlib

class File(models.Model):
    name = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=64, unique=True)
    content_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=512)
    folder = models.ForeignKey('Folder', null=True, blank=True, on_delete=models.SET_NULL)
    is_starred = models.BooleanField(default=False)
    is_trashed = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)
    
    def calculate_hash(self, file_content):
        """Calculate SHA-256 hash of file content"""
        sha256_hash = hashlib.sha256()
        for chunk in file_content.chunks():
            sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['file_hash']),
            models.Index(fields=['name']),
            models.Index(fields=['uploaded_at']),
        ]

class Folder(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
