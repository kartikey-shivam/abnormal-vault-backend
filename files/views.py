from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.conf import settings
import os
from .models import File
from .serializers import FileSerializer
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from django.http import FileResponse

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        try:
            if 'file' not in request.FILES:
                return Response(
                    {'error': 'No file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            file_obj = request.FILES['file']
            
            # Create File instance
            file_instance = File(
                name=file_obj.name,
                content_type=file_obj.content_type,
                size=file_obj.size,
                uploaded_by=request.user
            )
            
            # Calculate hash before saving
            file_hash = file_instance.calculate_hash(file_obj)
            
            # Check for duplicates
            existing_file = File.objects.filter(file_hash=file_hash).first()
            if existing_file:
                return Response(FileSerializer(existing_file).data)
            
            # Save new file
            file_instance.file_hash = file_hash
            file_instance.file_path = f'uploads/{file_hash}/{file_obj.name}'
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_instance.file_path), exist_ok=True)
            
            # Save file content
            with open(file_instance.file_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)
            
            file_instance.save()
            return Response(
                FileSerializer(file_instance).data, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_queryset(self):
        queryset = File.objects.all()
        
        # Implement search and filtering
        name = self.request.query_params.get('name', None)
        content_type = self.request.query_params.get('content_type', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        if date_from:
            queryset = queryset.filter(uploaded_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(uploaded_at__lte=date_to)
            
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def star(self, request, pk=None):
        file = self.get_object()
        file.is_starred = not file.is_starred
        file.save()
        return Response(FileSerializer(file).data)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        try:
            file = self.get_object()
            file_path = os.path.join(settings.BASE_DIR, file.file_path)
            
            if not os.path.exists(file_path):
                return Response(
                    {'error': 'File not found on server'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=file.name
            )
            response['Content-Type'] = file.content_type
            response['Content-Length'] = file.size
            return response
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_files = File.objects.filter(
            uploaded_by=request.user,
            is_trashed=False
        ).order_by('-uploaded_at')[:10]
        return Response(FileSerializer(recent_files, many=True).data)

    @action(detail=False, methods=['get'])
    def starred(self, request):
        starred_files = File.objects.filter(
            uploaded_by=request.user,
            is_starred=True,
            is_trashed=False
        )
        return Response(FileSerializer(starred_files, many=True).data)

    @action(detail=False, methods=['post'], url_path='check-duplicate')
    def check_duplicate(self, request):
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        file_obj = request.FILES['file']
        
        # Create temporary File instance to calculate hash
        temp_file = File(
            name=file_obj.name,
            content_type=file_obj.content_type,
            size=file_obj.size,
            uploaded_by=request.user
        )
        
        # Calculate hash
        file_hash = temp_file.calculate_hash(file_obj)
        
        # Check for existing file with same hash
        existing_file = File.objects.filter(file_hash=file_hash).first()
        
        if existing_file:
            return Response({
                'duplicate_found': True,
                'file': FileSerializer(existing_file).data
            })
        
        return Response({
            'duplicate_found': False
        })

class StorageViewSet(ViewSet):
    @action(detail=False, methods=['get'])
    def usage(self, request):
        total_size = File.objects.filter(
            uploaded_by=request.user,
            is_trashed=False
        ).aggregate(Sum('size'))['size__sum'] or 0
        
        return Response({
            'usage': total_size,
            'usage_formatted': f"{total_size / (1024*1024):.2f} MB"
        })

    @action(detail=False, methods=['get'])
    def quota(self, request):
        # Example quota of 1GB
        quota = 1024 * 1024 * 1024
        usage = File.objects.filter(
            uploaded_by=request.user,
            is_trashed=False
        ).aggregate(Sum('size'))['size__sum'] or 0
        
        return Response({
            'quota': quota,
            'usage': usage,
            'remaining': quota - usage,
            'percentage_used': (usage / quota) * 100
        })
