from typing import Dict
from apps.control_plane.app.bots.life_admin.bot import LifeAdminBot

_BOTS: Dict[str, object] = {
    "life_admin": LifeAdminBot(),
}

def get_bot(name: str):
    if name not in _BOTS:
        raise KeyError(f"Unknown bot: {name}")
    return _BOTS[name]

def list_bots():
    return list(_BOTS.keys())