from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    goal: str
    domain: str = "general"
    expected_output: str = ""
    inputs: List[str] = field(default_factory=list)
    required_tools: List[str] = field(default_factory=list)
    risk: str = "low"
    raw_text: str = ""


@dataclass
class Candidate:
    source_id: str
    kind: str
    title: str
    content: str
    similarity: float = 0.0
    human_approved: bool = False
    validator_passed: bool = False
    repeated_successes: int = 0
    recent_success: bool = False
    tool_compatible: bool = True
    recency_weight: float = 0.0
    version: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    score: float = 0.0


@dataclass
class AgentKnowledgePacket:
    task: Dict[str, Any]
    recommended_skill: Optional[Dict[str, Any]]
    rules: List[Dict[str, Any]] = field(default_factory=list)
    corrections: List[Dict[str, Any]] = field(default_factory=list)
    known_failures: List[Dict[str, Any]] = field(default_factory=list)
    required_tools: List[str] = field(default_factory=list)
    validation: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    source_ids: List[str] = field(default_factory=list)
    status: str = "OK"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
