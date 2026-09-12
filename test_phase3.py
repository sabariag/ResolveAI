from agents.orchestrator import AgentOrchestrator


def run_test(request):
    print("\n" + "=" * 70)
    print("REQUEST:", request)
    print("=" * 70)

    orchestrator = AgentOrchestrator()
    result = orchestrator.run(request)

    print("\nSTATUS:", result.get("status"))
    print("SELECTED AGENTS:", result.get("selected_agents"))

    print("\nDECISION:")
    print(result.get("result"))

    print("\nACTION RESULT:")
    print(result.get("action_result"))

    print("\nVERIFICATION:")
    print(result.get("verification"))


requests = [
    "My headphones arrived damaged and I want a replacement",
    "I want a refund for my order",
    "I want to cancel my order",
    "Do you have this product in stock?",
    "Which warehouse has the product?",
]

for request in requests:
    run_test(request)