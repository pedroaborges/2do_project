from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        from datetime import date, time, datetime, timedelta

        interval, _ = IntervalSchedule.objects.get_or_create(every=1, period='days')

        PeriodicTask.objects.filter(name='clearday_everyday_task').delete()

        clearday, _ = PeriodicTask.objects.get_or_create(
            name='clearday_everyday_task',
            task='tasks.tasks.delete_tasks',
            start_time= datetime.combine(date.today() + timedelta(days=1),time.fromisoformat('00:00')),
            interval_id=interval.id,
            description='Clears all task logs at the end of the day'
        )
        return super().ready()