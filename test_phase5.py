from agents.orchestrator import AgentOrchestrator


def test_phase5_baseline():

    orchestrator = AgentOrchestrator()

    result = orchestrator.run(
        "My headphones arrived damaged and I want a replacement"
    )

    print("\n" + "=" * 70)
    print("PHASE 5 BASELINE TEST")
    print("=" * 70)

    print("\nSTATUS:")
    print(result["status"])

    print("\nSELECTED AGENTS:")
    print(result["selected_agents"])

    print("\nDECISION:")
    print(result["result"])

    print("\nACTION RESULT:")
    print(result["action_result"])

    print("\nVERIFICATION:")
    print(result["verification"])

    print("\nHISTORY:")
    for item in result["history"]:
        print(item)


if __name__ == "__main__":
    test_phase5_baseline()