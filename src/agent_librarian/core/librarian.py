from __future__ import annotations

from agent_librarian.adapters.agentvallet import AgentValletAdapter
from agent_librarian.context.packet_builder import PacketBuilder
from agent_librarian.core.query_builder import QueryBuilder
from agent_librarian.core.task_interpreter import TaskInterpreter
from agent_librarian.ranking.ranker import CandidateRanker
from agent_librarian.schemas.models import AgentKnowledgePacket


class AgentLibrarian:
    """Universal retrieval-and-reuse agent.

    It does not perform the business task. It prepares the best available
    knowledge package for the working agent.
    """

    def __init__(
        self,
        agentvallet: AgentValletAdapter,
        interpreter: TaskInterpreter | None = None,
        query_builder: QueryBuilder | None = None,
        ranker: CandidateRanker | None = None,
        packet_builder: PacketBuilder | None = None,
    ) -> None:
        self.agentvallet = agentvallet
        self.interpreter = interpreter or TaskInterpreter()
        self.query_builder = query_builder or QueryBuilder()
        self.ranker = ranker or CandidateRanker()
        self.packet_builder = packet_builder or PacketBuilder()

    def prepare(self, task_text: str) -> AgentKnowledgePacket:
        task = self.interpreter.interpret(task_text)
        queries = self.query_builder.build(task)
        candidates = self.agentvallet.search(queries=queries, task=task)
        ranked = self.ranker.rank(candidates)
        return self.packet_builder.build(task=task, ranked=ranked)
