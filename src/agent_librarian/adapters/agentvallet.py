from __future__ import annotations

from typing import Protocol, Sequence
from agent_librarian.schemas.models import Candidate, Task


class AgentValletAdapter(Protocol):
    """Minimal contract AgentLibrarian needs from AgentVallet."""

    def search(self, queries: Sequence[str], task: Task) -> list[Candidate]:
        ...


class InMemoryAgentValletAdapter:
    """Tiny development adapter used for tests and examples."""

    def __init__(self, candidates: list[Candidate] | None = None):
        self._candidates = candidates or []

    def search(self, queries: Sequence[str], task: Task) -> list[Candidate]:
        terms = {token.lower() for q in queries for token in q.split() if len(token) > 2}
        out: list[Candidate] = []
        for candidate in self._candidates:
            haystack = f"{candidate.title} {candidate.content}".lower()
            overlap = sum(1 for term in terms if term in haystack)
            candidate.similarity = min(1.0, overlap / max(1, min(len(terms), 8)))
            out.append(candidate)
        return out
