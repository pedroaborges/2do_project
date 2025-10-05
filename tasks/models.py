from django.contrib.auth.models import User
from django.db import models

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