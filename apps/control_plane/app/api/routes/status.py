from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from redis import Redis

from apps.control_plane.app.db.session import get_db
from apps.control_plane.app.core.config import settings

router = APIRouter()

def redis_client() -> Redis:
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)

@router.get("/status")
def status(db: Session = Depends(get_db)):
    # DB check
    db.execute(text("SELECT 1"))

    # Redis check
    r = redis_client()
    pong = r.ping()

    return {
        "db": "ok",
        "redis": "ok" if pong else "down",
        "env": settings.ENV,
    }