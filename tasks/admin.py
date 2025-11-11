from django.contrib import admin
from .models import Task, EmailVerification

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'description', 'category', 'init_hour', 'end_hour', 'status')
    search_fields = ('name',)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'temp_email', 'token', 'is_verified')
    search_fields = ('user',)