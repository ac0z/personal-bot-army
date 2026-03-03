from dataclasses import dataclass
from typing import Protocol, Any

@dataclass(frozen=True)
class BotContext:
    request_id: str

class Bot(Protocol):
    name: str

    def register_jobs(self) -> None:
        """Define recurring schedules / one-off jobs. Called on startup (or manually)."""
        ...

    def run(self, job_name: str, **kwargs: Any) -> dict:
        """Execute a specific job and return meta dict (for RunHistory)."""
        ...