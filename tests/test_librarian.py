from agent_librarian import AgentLibrarian, Candidate
from agent_librarian.adapters.agentvallet import InMemoryAgentValletAdapter


def test_prefers_validated_human_approved_skill():
    candidates = [
        Candidate(
            source_id="raw-1",
            kind="skill",
            title="Bank reconciliation draft",
            content="Draft approach",
            similarity=0.9,
        ),
        Candidate(
            source_id="skill-7",
            kind="skill",
            title="Approved bank reconciliation",
            content="Use validated reconciliation workflow",
            human_approved=True,
            validator_passed=True,
            repeated_successes=4,
            recent_success=True,
            version="v7",
        ),
        Candidate(
            source_id="corr-2",
            kind="correction",
            title="Refund correction",
            content="Ignore CAB-DD liquidation when calculating refund",
            human_approved=True,
            validator_passed=True,
        ),
    ]

    librarian = AgentLibrarian(InMemoryAgentValletAdapter(candidates))
    packet = librarian.prepare("Do bank reconciliation for this office")

    assert packet.status == "OK"
    assert packet.recommended_skill is not None
    assert packet.recommended_skill["source_id"] == "skill-7"
    assert packet.corrections[0]["source_id"] == "corr-2"


def test_returns_no_reliable_match_when_vault_has_no_candidates():
    librarian = AgentLibrarian(InMemoryAgentValletAdapter([]))
    packet = librarian.prepare("Completely new task")
    assert packet.status == "NO_RELIABLE_MATCH"
    assert packet.recommended_skill is None
