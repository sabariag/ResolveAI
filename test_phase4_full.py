from agents.orchestrator import AgentOrchestrator
from agents.mock_agents import MockOrderAgent
from agents.decision_agent import DecisionAgent
from agents.base_agent import BaseAgent


class RetryInventoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("inventory")
        self.attempts = 0

    def run(self, task):
        self.attempts += 1

        if self.attempts == 1:
            return {
                "agent": self.name,
                "status": "failed",
                "error": "Temporary inventory service failure",
            }

        return {
            "agent": self.name,
            "status": "success",
            "data": {
                "product": "Headphones",
                "available": True,
                "warehouse": "WH-01",
            },
        }


def test_full_retry_workflow():

    orchestrator = AgentOrchestrator(
        agents=[
            MockOrderAgent(),
            RetryInventoryAgent(),
            DecisionAgent(),
        ]
    )

    result = orchestrator.run(
        "My headphones arrived damaged and I want a replacement"
    )

    print("\n" + "=" * 70)
    print("PHASE 4.4 FULL RETRY WORKFLOW TEST")
    print("=" * 70)

    print("\nSTATUS:")
    print(result["status"])

    print("\nAGENT RESULTS:")
    print(result["agent_results"])

    print("\nDECISION:")
    print(result["result"])

    print("\nHISTORY:")
    for item in result["history"]:
        print(item)

    retry_entries = [
        item
        for item in result["history"]
        if item.get("step") == "retry"
    ]

    assert len(retry_entries) == 1
    assert retry_entries[0]["agent"] == "inventory"
    assert retry_entries[0]["attempt"] == 2
    assert retry_entries[0]["status"] == "success"

    assert result["agent_results"]["inventory"]["retry"] is True
    assert result["agent_results"]["inventory"]["attempt"] == 2

    print("\n✅ Phase 4.4 full retry workflow test passed!")


if __name__ == "__main__":
    test_full_retry_workflow()