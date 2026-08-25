from .celery_app import celery_app


@celery_app.task
def test_task():
    print("🔥 Celery task is running!")

    return {
        "message": "Celery is working successfully"
    }