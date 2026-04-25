from celery.schedules import crontab

# Celery beat schedule for fetching Deribit prices every minute
beat_schedule = {
    "fetch-deribit-prices-every-minute": {
        "task": "app.price.tasks.fetch_deribit_prices",
        "schedule": 60.0,  # Run every 60 seconds (1 minute)
        "options": {"queue": "prices"},
    },
}

# Timezone for the scheduler
timezone = "UTC"
