from agent_librarian import AgentLibrarian, Candidate
from agent_librarian.adapters.agentvallet import InMemoryAgentValletAdapter


vault = InMemoryAgentValletAdapter([
    Candidate(
        source_id="skill-bank-reco-v1",
        kind="skill",
        title="Validated bank reconciliation",
        content="Match statement totals, classify exceptions, validate closing balance.",
        human_approved=True,
        validator_passed=True,
        repeated_successes=5,
        recent_success=True,
        version="v1",
    ),
    Candidate(
        source_id="corr-refund-1",
        kind="correction",
        title="Refund classification correction",
        content="Ignore CAB-DD liquidation when calculating refund received.",
        human_approved=True,
        validator_passed=True,
    ),
])

librarian = AgentLibrarian(vault)
packet = librarian.prepare("Do bank reconciliation for this office")
print(packet.to_dict())
