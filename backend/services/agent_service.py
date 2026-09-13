from agents.orchestrator import AgentOrchestrator


class AgentService:

    def __init__(self):
        self.orchestrator = AgentOrchestrator()

    async def process_query(self, payload):
        customer_request = payload.get("query", "")

        if not customer_request:
            return {
                "status": "error",
                "message": "Query is required"
            }

        result = self.orchestrator.run(customer_request)

        return result


agent_service = AgentService()