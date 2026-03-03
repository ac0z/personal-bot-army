from fastapi import APIRouter
from apps.control_plane.app.bots.registry import list_bots
from apps.control_plane.app.jobs.queue import get_queue
from apps.control_plane.app.jobs.scheduler import ensure_schedules

router = APIRouter()

@router.get("")
def get_bots():
    return {"bots": list_bots()}

@router.post("/schedules/ensure")
def schedules_ensure():
    ensure_schedules()
    return {"ok": True}

@router.post("/{bot_name}/{job_name}/run")
def run_job(bot_name: str, job_name: str):
    q = get_queue("default")
    job = q.enqueue("apps.control_plane.app.jobs.tasks.run_bot_job", bot_name, job_name)
    return {"enqueued": True, "job_id": job.id}