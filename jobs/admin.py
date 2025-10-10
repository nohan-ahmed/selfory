from django.contrib import admin
from .models import Job, AIModel

# Register your models here.

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job_type', 'status', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('job_type', 'status', 'created_at')
    ordering = ('-created_at',)


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'credits_cost', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)