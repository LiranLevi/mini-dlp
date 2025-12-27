import os
from celery import Celery

REDIS_URL = os.environ["REDIS_URL"]

celery_app = Celery(
  "scanner",
  broker=REDIS_URL,
  backend=REDIS_URL,
  include=["app.tasks"],
)

celery_app.conf.task_default_queue = "scan_jobs"