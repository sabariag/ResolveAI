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


def test_retry():

    retry_agent = RetryTestAgent()

    orchestrator = AgentOrchestrator(
        agents=[retry_agent]
    )

    result = orchestrator.execute_agents(
        ["test_agent"],
        "Test retry mechanism",
    )

    print("\n" + "=" * 70)
    print("PHASE 4.2 RETRY TEST")
    print("=" * 70)

    print("\nRESULT:")
    print(result)

    assert result["test_agent"]["status"] == "success"
    assert result["test_agent"]["retry"] is True
    assert result["test_agent"]["attempt"] == 2
    assert retry_agent.attempts == 2

    print("\n✅ Phase 4.2 retry test passed!")


if __name__ == "__main__":
    test_retry()