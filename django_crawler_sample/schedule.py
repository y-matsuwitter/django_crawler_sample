from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    'run_all_crawler_schedule': {
        'task': 'crawler.tasks.run_all_crawler',
        'schedule': crontab(minute='*/2'),
    },
}
