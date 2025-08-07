from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
import uuid

class SignalType(Enum):
    USER_INPUT = auto()
    PLUGIN_CALL = auto()
    SYSTEM_EVENT = auto()

class ActionStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    DONE = auto()
    FAILED = auto()

@dataclass
class Signal:
    name: str
    payload: dict
    context: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: SignalType = SignalType.USER_INPUT
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Action:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    target: str = ""
    params: dict = field(default_factory=dict)
    status: ActionStatus = field(default_factory=lambda: ActionStatus.PENDING)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
