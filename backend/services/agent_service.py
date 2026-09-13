from agents.orchestrator import AgentOrchestrator


class AgentService:
    def __init__(self):
        self.orchestrator = AgentOrchestrator()

    async def process_query(self, payload):
        query = payload.get("query", "")

        if not query:
            return {
                "status": "error",
                "message": "Query is required"
            }

        return self.orchestrator.run(query)


agent_service = AgentService()