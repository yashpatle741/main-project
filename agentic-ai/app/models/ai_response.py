from dataclasses import dataclass


@dataclass
class AIResponse:
    root_cause: str
    confidence: int
    action: str
    deployment: str
    reason: str