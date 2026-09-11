from __future__ import annotations

from agent_librarian.schemas.models import Candidate


class CandidateRanker:
    """Deterministic trust + relevance scorer.

    Score intentionally keeps trust rules outside the LLM.
    """

    def score(self, candidate: Candidate) -> float:
        score = 0.0
        score += 30.0 if candidate.human_approved else 0.0
        score += 25.0 if candidate.validator_passed else 0.0
        score += 20.0 * max(0.0, min(1.0, candidate.similarity))
        score += 10.0 if candidate.recent_success else 0.0
        score += min(10.0, candidate.repeated_successes * 2.0)
        score += 5.0 if candidate.tool_compatible else 0.0
        score += max(0.0, min(5.0, candidate.recency_weight * 5.0))
        candidate.score = round(score, 2)
        return candidate.score

    def rank(self, candidates: list[Candidate]) -> list[Candidate]:
        for candidate in candidates:
            self.score(candidate)
        return sorted(candidates, key=lambda item: item.score, reverse=True)
