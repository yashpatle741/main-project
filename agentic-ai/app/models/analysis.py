from dataclasses import dataclass, field


@dataclass
class AnalysisReport:
    namespace: str
    pod: str
    issue: str
    logs: str = ""
    events: list[dict] = field(default_factory=list)