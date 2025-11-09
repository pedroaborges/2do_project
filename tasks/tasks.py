from datetime import datetime, timedelta
from celery import shared_task
from .models import Task, User
from django_celery_beat.models import (PeriodicTask, ClockedSchedule)
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

@shared_task
def deactive_task(id_task):
    task = Task.objects.get(id=id_task)
    task.status = True
    task.save()

    email = User.objects.get(id=task.owner.id).email

    subject = '2DO notification - Tarefa desativada'
    message = render_to_string('taskDeactivated.html', {
        'taskName': task.name,
        'time': timezone.localtime(timezone.now()).time(),
    })

    send_async_email(subject=subject, html_message=message, recipient_list=[email])

@shared_task
def delete_tasks():
    tasks = Task.objects.all()
    users = User.objects.filter(id__in=list(tasks.values_list('owner', flat=True)))
    tasks.delete()
    ClockedSchedule.objects.all().delete()
    PeriodicTask.objects.filter(task='tasks.tasks.deactive_task').delete()

    emails = users.values_list('email', flat=True)
    emails = list(emails)

    subject = '2DO notification - Tarefas deletadas'
    message = render_to_string('tasksDeleted.html', {
        'time': timezone.localtime(timezone.now()).time(),
    })

    send_async_email(subject=subject, html_message=message, recipient_list=emails)

@shared_task
def send_async_email(subject, html_message, recipient_list):
    send_mail(subject=subject, html_message=html_message, message=html_message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list)