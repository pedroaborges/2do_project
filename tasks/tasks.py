from celery import shared_task
from .models import Task
from django_celery_beat.models import (PeriodicTask, ClockedSchedule)

@shared_task
def deactive_task(id_task):
    task = Task.objects.get(id=id_task)
    task.status = True
    task.save()

@shared_task
def delete_tasks():
    Task.objects.all().delete()
    ClockedSchedule.objects.all().delete()
    PeriodicTask.objects.filter(task='tasks.tasks.deactive_task').delete()