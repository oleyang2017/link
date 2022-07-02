from celery import Celery

celery_app = Celery("link-services", broker="redis://link_redis:6379/1")
celery_app.autodiscover_tasks(["services.tasks.device"], "task")
