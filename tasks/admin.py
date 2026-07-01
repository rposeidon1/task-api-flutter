from django.contrib import admin
from tasks.models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "completed", "created_at"]
    list_filter = ["completed", "owner"]
    search_fields = ["title", "description"]