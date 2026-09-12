from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

result = orchestrator.run(
    "My headphones arrived damaged and I want a replacement"
)

print("\nFINAL RESULT:")
print(result)