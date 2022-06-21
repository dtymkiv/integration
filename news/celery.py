import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsapp.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')
print("HEREERERERERRE")
app.autodiscover_tasks()
