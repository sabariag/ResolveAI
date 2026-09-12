from agents.decision_agent import DecisionAgent


def test_failed_agent():

    decision_agent = DecisionAgent()

    task = {
        "customer_request": (
            "My headphones arrived damaged and I want a replacement"
        ),
        "agent_results": {
            "order": {
                "agent": "order",
                "status": "success",
                "data": {
                    "order_id": "ORD-1001",
                    "product": "Headphones",
                    "condition": "damaged",
                },
            },
            "policy": {
                "agent": "policy",
                "status": "success",
                "data": {
                    "replacement_allowed": True,
                },
            },
            "inventory": {
                "agent": "inventory",
                "status": "failed",
                "error": "Inventory service unavailable",
            },
        },
    }

    result = decision_agent.run(task)

    print("\n" + "=" * 70)
    print("PHASE 4 TEST")
    print("=" * 70)

    print("\nDECISION:")
    print(result)

    assert result["decision"] == "NEEDS_REVIEW"

    print("\n✅ Phase 4.1 test passed!")


if __name__ == "__main__":
    test_failed_agent()