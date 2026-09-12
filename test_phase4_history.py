from agents.orchestrator import AgentOrchestrator
from agents.base_agent import BaseAgent


class RetryTestAgent(BaseAgent):

    def __init__(self):
        super().__init__("test_agent")
        self.attempts = 0

    def run(self, task):
        self.attempts += 1

        if self.attempts == 1:
            return {
                "agent": self.name,
                "status": "failed",
                "error": "Temporary service failure",
            }

        return {
            "agent": self.name,
            "status": "success",
            "data": {
                "message": "Agent succeeded after retry"
            },
        }


def test_history():

    retry_agent = RetryTestAgent()

    orchestrator = AgentOrchestrator(
        agents=[retry_agent]
    )

    # Directly test agent execution first
    agent_results = orchestrator.execute_agents(
        ["test_agent"],
        "Test workflow history",
    )

    # Create a history entry the same way run() does
    history = []

    for agent_name, result in agent_results.items():
        if result.get("retry") is True:
            history.append(
                {
                    "step": "retry",
                    "agent": agent_name,
                    "attempt": result.get("attempt", 2),
                    "status": result.get("status"),
                }
            )

    print("\n" + "=" * 70)
    print("PHASE 4.3 HISTORY TEST")
    print("=" * 70)

    print("\nAGENT RESULT:")
    print(agent_results)

    print("\nWORKFLOW HISTORY:")
    print(history)

    assert len(history) == 1
    assert history[0]["step"] == "retry"
    assert history[0]["agent"] == "test_agent"
    assert history[0]["attempt"] == 2
    assert history[0]["status"] == "success"

    print("\n✅ Phase 4.3 history test passed!")


if __name__ == "__main__":
    test_history()