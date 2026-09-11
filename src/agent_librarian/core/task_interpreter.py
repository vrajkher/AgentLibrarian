from __future__ import annotations

import re
from agent_librarian.schemas.models import Task


class TaskInterpreter:
    """Deterministic MVP task parser.

    A model-backed interpreter can replace or extend this later without
    changing the public contract.
    """

    DOMAIN_HINTS = {
        "accounting": ("bank", "ledger", "reconciliation", "invoice", "payment", "receipt"),
        "tax": ("gst", "tds", "tax", "return"),
        "coding": ("code", "repo", "github", "python", "api", "bug"),
        "email": ("email", "mail", "draft", "reply"),
    }

    def interpret(self, text: str) -> Task:
        cleaned = re.sub(r"\s+", " ", text).strip()
        lower = cleaned.lower()
        domain = "general"
        for name, hints in self.DOMAIN_HINTS.items():
            if any(hint in lower for hint in hints):
                domain = name
                break

        expected_output = ""
        if "report" in lower:
            expected_output = "report"
        elif "email" in lower or "mail" in lower:
            expected_output = "email"
        elif "reconciliation" in lower or "reconcile" in lower:
            expected_output = "reconciliation_result"

        risk = "medium" if any(x in lower for x in ("send", "delete", "pay", "file return", "submit")) else "low"

        return Task(
            goal=cleaned,
            domain=domain,
            expected_output=expected_output,
            risk=risk,
            raw_text=text,
        )
