from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Job, AIModel
from .serializers import JobSerializer, AIModelSerializer
from core.permissions import IsOwnerOrReadOnly
from jobs.tasks import content_generation_task
# Create your views here.

class JobViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
    def perform_create(self, serializer):
        job = serializer.save(user=self.request.user)
        content_generation_task.delay(job_id=job.id)
        
    def perform_update(self, serializer):
        job = serializer.save(user=self.request.user)
        content_generation_task.delay(job_id=job.id)