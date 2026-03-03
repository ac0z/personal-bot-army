import uuid
from sqlalchemy import update
from sqlalchemy.orm import Session
from apps.control_plane.app.db.session import SessionLocal
from apps.control_plane.app.db.models.run_history import RunHistory
from apps.control_plane.app.bots.registry import get_bot

def run_bot_job(bot_name: str, job_name: str, **kwargs):
    request_id = str(uuid.uuid4())

    db: Session = SessionLocal()
    run = RunHistory(bot_name=bot_name, run_type=job_name, status="started", meta={"request_id": request_id})
    db.add(run)
    db.commit()
    db.refresh(run)

    try:
        bot = get_bot(bot_name)
        meta = bot.run(job_name, **kwargs)
        run.status = "success"
        run.meta = {**(run.meta or {}), **(meta or {})}
        run.finished_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        db.commit()
        return {"ok": True, "run_id": run.id, "meta": run.meta}
    except Exception as e:
        run.status = "failed"
        run.meta = {**(run.meta or {}), "error": str(e)}
        run.finished_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        db.commit()
        raise
    finally:
        db.close()