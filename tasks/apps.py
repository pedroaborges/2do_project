from django.apps import AppConfig
from django.db.models.signals import post_migrate

def PeriodicTaskConfig(sender, **kwargs):
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    from datetime import date, time, datetime, timedelta
    from django.utils import timezone

    interval, _ = IntervalSchedule.objects.get_or_create(every=1, period='days')

    PeriodicTask.objects.filter(name='clearday_everyday_task').delete()

    clearday, _ = PeriodicTask.objects.get_or_create(
        name='clearday_everyday_task',
        task='tasks.tasks.delete_tasks',
        start_time= timezone.localtime(timezone.make_aware(datetime.combine(date.today() + timedelta(days=1),time.fromisoformat('00:00')), timezone.get_current_timezone())),
        interval_id=interval.id,
        description='Clears all task logs at the end of the day'
    )

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        post_migrate.connect(PeriodicTaskConfig)
        return super().ready()