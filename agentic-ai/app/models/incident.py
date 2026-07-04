from dataclasses import dataclass


@dataclass
class Incident:
    namespace: str
    pod: str
    issue: str