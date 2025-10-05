from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'description', 'category', 'init_hour', 'end_hour', 'status')
    search_fields = ('name',)