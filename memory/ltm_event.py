from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List
import uuid




class LTMEventType(Enum):
    FACT = "fact"
    EXPERIENCE = "experience"
    EMOTION = "emotion"
    RELATION = "relation"
    SYSTEM = "system"

class MemorySource(Enum):
    USER = "user"
    SELF = "self"
    SYSTEM = "system"



@dataclass
class LTMEvent:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    type: LTMEventType = LTMEventType.FACT
    source: MemorySource = MemorySource.SYSTEM

    content: str = ""

    importance: float = 0.5        # poznawcza ważność (0–1)
    emotional_weight: float = 0.0  # ślad afektywny (-1–1)
    confidence: float = 1.0        # jak „pewne” jest to wspomnienie

    tags: List[str] = field(default_factory=list)

    vector: Optional[list[float]] = None  # placeholder pod embedding

    created_at: datetime = field(default_factory=datetime.utcnow)
    last_accessed: Optional[datetime] = None

    timestamp: datetime = datetime.utcnow()

