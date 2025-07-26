import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_movie.settings')

app = Celery('django_movie')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Configuration Options
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    result_backend='redis://localhost:6379/0',
    broker_url='redis://localhost:6379/0',
    task_always_eager=False,
    task_eager_propagates=True,
    task_ignore_result=False,
    task_store_eager_result=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,
    task_compression='gzip',
    result_compression='gzip',
    task_routes={
        'movies.tasks.send_order_notification': {'queue': 'notifications'},
        'movies.tasks.send_email_notification': {'queue': 'notifications'},
        'movies.tasks.cleanup_old_data': {'queue': 'maintenance'},
        'movies.tasks.generate_product_recommendations': {'queue': 'recommendations'},
    },
    beat_schedule={
        'cleanup-old-data': {
            'task': 'movies.tasks.cleanup_old_data',
            'schedule': 86400.0,  # Run daily
        },
    },
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')