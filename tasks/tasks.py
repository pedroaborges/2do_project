from celery import shared_task
from .models import Task

@shared_task
def deactive_task(id_task):
    task = Task.objects.get(id=id_task)
    task.status = True
    task.save()

@shared_task
def delete_task():
    task = Task.objects.all()
    task.delete()