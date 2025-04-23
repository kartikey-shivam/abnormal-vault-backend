from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='content_type')
    modifiedAt = serializers.DateTimeField(source='uploaded_at', format="%Y-%m-%dT%H:%M:%SZ")
    createdAt = serializers.DateTimeField(source='uploaded_at', format="%Y-%m-%dT%H:%M:%SZ")
    starred = serializers.BooleanField(source='is_starred')
    shared = serializers.SerializerMethodField()
    # url = serializers.SerializerMethodField()
    folder_id = serializers.PrimaryKeyRelatedField(source='folder', read_only=True)
    trashed = serializers.BooleanField(source='is_trashed')
    trashedAt = serializers.DateTimeField(source='trashed_at', format="%Y-%m-%dT%H:%M:%SZ")
    # owner = serializers.SerializerMethodField()
    # hash = serializers.CharField(source='file_hash')

    class Meta:
        model = File
        fields = [
            'id', 'name', 'type', 'size', 'modifiedAt', 'createdAt',
            'starred', 'shared', 'folder_id', 'trashed',
            'trashedAt'
        ]

    def get_shared(self, obj):
        # Implement sharing logic here if needed
        return False

    # def get_url(self, obj):
    #     request = self.context.get('request')
    #     if request and obj.file_path:
    #         return request.build_absolute_uri(f'/api/files/{obj.id}/download/')
    #     return None

    # def get_owner(self, obj):
    #     return {
    #         'id': obj.uploaded_by.id,
    #         'username': obj.uploaded_by.username,
    #         'email': obj.uploaded_by.email
    #     }