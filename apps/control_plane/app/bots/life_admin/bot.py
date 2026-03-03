from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select

from apps.control_plane.app.core.notifications import notifier
from apps.control_plane.app.db.session import SessionLocal
from apps.control_plane.app.db.models.subscription import Subscription

class LifeAdminBot:
    name = "life_admin"

    def register_jobs(self) -> None:
        # Scheduling'i rqscheduler üzerinden yapacağız (scheduler.py)
        return

    def run(self, job_name: str, **kwargs) -> dict:
        if job_name == "renewal_scan":
            return self._renewal_scan()
        if job_name == "weekly_digest":
            return self._weekly_digest()
        raise ValueError(f"Unknown job_name: {job_name}")

    def _renewal_scan(self) -> dict:
        db: Session = SessionLocal()
        try:
            now = datetime.now(timezone.utc)
            horizon = now + timedelta(days=3)

            q = select(Subscription).where(
                Subscription.is_active == True,
                Subscription.renew_at <= horizon
            )
            rows = db.execute(q).scalars().all()

            count = 0
            for s in rows:
                count += 1
                msg = f"⏰ Yenileme yaklaşıyor: {s.title}\nTarih: {s.renew_at.isoformat()}"
                # Telegram anlık
                import asyncio
                asyncio.run(notifier.telegram_send(msg))

            return {"near_due_count": count}
        finally:
            db.close()

    def _weekly_digest(self) -> dict:
        # Email haftalık özet (basit örnek)
        db: Session = SessionLocal()
        try:
            q = select(Subscription).where(Subscription.is_active == True)
            rows = db.execute(q).scalars().all()

            lines = ["Weekly Life Admin Summary", "------------------------"]
            for s in rows:
                lines.append(f"- {s.title} | renew_at={s.renew_at.isoformat()} | active={s.is_active}")

            notifier.email_send("Life Admin - Weekly Summary", "\n".join(lines))
            return {"subscriptions_count": len(rows), "email_sent": True}
        finally:
            db.close()