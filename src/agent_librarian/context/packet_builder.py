from __future__ import annotations

from dataclasses import asdict
from agent_librarian.schemas.models import AgentKnowledgePacket, Candidate, Task


class PacketBuilder:
    def build(self, task: Task, ranked: list[Candidate], minimum_confidence: float = 50.0) -> AgentKnowledgePacket:
        if not ranked or ranked[0].score < minimum_confidence:
            return AgentKnowledgePacket(
                task=asdict(task),
                recommended_skill=None,
                required_tools=task.required_tools,
                confidence=ranked[0].score if ranked else 0.0,
                source_ids=[c.source_id for c in ranked[:3]],
                status="NO_RELIABLE_MATCH",
            )

        top = ranked[0]
        rules = []
        corrections = []
        failures = []
        validation = []

        for candidate in ranked[:8]:
            item = {
                "source_id": candidate.source_id,
                "title": candidate.title,
                "content": candidate.content,
                "score": candidate.score,
            }
            if candidate.kind == "rule":
                rules.append(item)
            elif candidate.kind == "correction":
                corrections.append(item)
            elif candidate.kind == "failure":
                failures.append(item)
            elif candidate.kind == "validation":
                validation.append(item)

        recommended_skill = None
        skill = next((c for c in ranked if c.kind == "skill"), None)
        if skill:
            recommended_skill = {
                "source_id": skill.source_id,
                "title": skill.title,
                "content": skill.content,
                "version": skill.version,
                "score": skill.score,
            }

        return AgentKnowledgePacket(
            task=asdict(task),
            recommended_skill=recommended_skill,
            rules=rules[:3],
            corrections=corrections[:3],
            known_failures=failures[:3],
            required_tools=task.required_tools,
            validation=validation[:3],
            confidence=top.score,
            source_ids=[c.source_id for c in ranked[:8]],
            status="OK",
        )
