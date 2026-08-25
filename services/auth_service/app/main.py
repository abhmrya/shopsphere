from fastapi import FastAPI

from services.auth_service.app.workers.tasks import test_task


app = FastAPI(
    title="ShopSphere Auth Service",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/test-celery")
def test_celery():
    task = test_task.delay()

    return {
        "status":"ok",
        "message": "Task submitted successfully",
        "task_id": task.id,
    }