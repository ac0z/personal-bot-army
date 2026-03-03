from apps.control_plane.app.db.base import Base
from apps.control_plane.app.db.session import engine

# Modelleri import et ki metadata'ya yüklensin
from apps.control_plane.app.db.models.run_history import RunHistory  # noqa: F401
from apps.control_plane.app.db.models.subscription import Subscription  # noqa: F401

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)