from django.db import models
from users.models import User
from . import constants
# Create your models here.

class AIModel(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "Stable Diffusion v1"
    endpoint = models.URLField(blank=True, null=True)  # API endpoint for this model
    credits_cost = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Job(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_jobs')
    ai_model = models.ForeignKey(to=AIModel, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=100, choices=constants.JOB_TYPES, default='image') # e.g., "Image Generation"
    input_prompt = models.TextField()
    final_prompt = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=constants.JOB_STATUS, default='pending')
    const_credits = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.job_type}"