from redis import Redis
from rq import Queue
from apps.control_plane.app.core.config import settings

def get_redis() -> Redis:
    return Redis.from_url(settings.REDIS_URL)

def get_queue(name: str | None = None) -> Queue:
    return Queue(name or settings.RQ_DEFAULT_QUEUE, connection=get_redis())