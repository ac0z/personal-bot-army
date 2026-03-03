from rq import Queue
from rq_scheduler import Scheduler
from apps.control_plane.app.jobs.queue import get_redis
from datetime import timedelta

def ensure_schedules():
    redis = get_redis()
    q = Queue("default", connection=redis)
    s = Scheduler(queue=q, connection=redis)

    # renewal_scan: her 1 saatte bir
    s.schedule(
        scheduled_time=None,
        func="apps.control_plane.app.jobs.tasks.run_bot_job",
        args=["life_admin", "renewal_scan"],
        interval=int(timedelta(hours=1).total_seconds()),
        repeat=None,
        meta={"name": "life_admin:renewal_scan"},
    )

    # weekly_digest: 7 günde bir
    s.schedule(
        scheduled_time=None,
        func="apps.control_plane.app.jobs.tasks.run_bot_job",
        args=["life_admin", "weekly_digest"],
        interval=int(timedelta(days=7).total_seconds()),
        repeat=None,
        meta={"name": "life_admin:weekly_digest"},
    )