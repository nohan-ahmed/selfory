from rest_framework import serializers
from .models import Job, AIModel

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('id', 'user', 'final_prompt', 'status', 'const_credits', 'created_at', 'updated_at')
        
        
class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')