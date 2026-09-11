from __future__ import annotations

from agent_librarian.schemas.models import Task


class QueryBuilder:
    def build(self, task: Task) -> list[str]:
        queries = [task.goal]
        if task.domain != "general":
            queries.append(f"{task.domain} {task.goal}")
        if task.expected_output:
            queries.append(f"{task.expected_output} {task.goal}")
        queries.extend([
            f"validated skill {task.goal}",
            f"correction {task.goal}",
            f"known failure {task.goal}",
        ])
        # preserve order while deduplicating
        return list(dict.fromkeys(q.strip() for q in queries if q.strip()))
