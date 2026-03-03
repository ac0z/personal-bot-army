from datetime import datetime, timezone, timedelta
from rq import Queue
from rq_scheduler import Scheduler

from apps.control_plane.app.jobs.queue import get_redis

def _exists(s: Scheduler, name: str) -> bool:
    # rq-scheduler job'ları meta içinde saklıyor
    for j in s.get_jobs():
        if (j.meta or {}).get("name") == name:
            return True
    return False

def ensure_schedules() -> dict:
    redis = get_redis()
    q = Queue("default", connection=redis)
    s = Scheduler(queue=q, connection=redis)

    now = datetime.now(timezone.utc)

    created = []
    skipped = []

    # 1) renewal_scan: hourly
    name1 = "life_admin:renewal_scan"
    if _exists(s, name1):
        skipped.append(name1)
    else:
        s.schedule(
            scheduled_time=now + timedelta(seconds=5),
            func="apps.control_plane.app.jobs.tasks.run_bot_job",
            args=["life_admin", "renewal_scan"],
            interval=int(timedelta(hours=1).total_seconds()),
            repeat=None,
            meta={"name": name1},
        )
        created.append(name1)

    # 2) weekly_digest: weekly
    name2 = "life_admin:weekly_digest"
    if _exists(s, name2):
        skipped.append(name2)
    else:
        s.schedule(
            scheduled_time=now + timedelta(seconds=10),
            func="apps.control_plane.app.jobs.tasks.run_bot_job",
            args=["life_admin", "weekly_digest"],
            interval=int(timedelta(days=7).total_seconds()),
            repeat=None,
            meta={"name": name2},
        )
        created.append(name2)

    return {"created": created, "skipped": skipped}