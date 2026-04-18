from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class CompetencyFlag(Enum):
    VISION = "vision"
    ENTREPRENEURSHIP = "entrepreneurship"
    PASSION = "passion"
    TRUST = "trust"

@dataclass
class StateUpdate:
    stagnation_counter: int = 0
    competencies_covered: list[CompetencyFlag] = field(default_factory=list)
    rapport_score: float = 0.5
    last_topic: str = ""
    injection_fired: bool = False

@dataclass
class NPCResponse:
    assistant_message: str
    state_update: StateUpdate
    safety_flags: list[str]
