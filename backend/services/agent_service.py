class AgentService:

    async def process_query(self, payload):
        return {
            "status": "pending",
            "message": "Agent orchestration module not connected yet"
        }

agent_service = AgentService()
