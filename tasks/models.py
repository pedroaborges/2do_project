from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class Task(models.Model):
    categories = [
        ('Trabalho', 'Trabalho'),
        ('Esportes', 'Esportes'),
        ('Estudos', 'Estudos'),
        ('Lazer', 'Lazer'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=25, choices=categories)
    init_hour = models.TimeField(blank=False, null=False)
    end_hour = models.TimeField(blank=False, null=False)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['init_hour']

    def __str__(self):
        return self.name

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    temp_email = models.EmailField(unique=True, default="")
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Verificação de e-mail para {self.user.email}"

    @staticmethod
    def generate_token():
        return str(uuid.uuid4())

    def is_expired(self):
        expiration_time = timezone.localtime(self.updated_at) + timedelta(minutes=15)
        return timezone.localtime(timezone.now()) > expiration_time
