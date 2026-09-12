from typing import Any, Dict, List

from agents.base_agent import BaseAgent
from agents.mock_agents import (
    MockOrderAgent,
    MockPolicyAgent,
    MockInventoryAgent,
)
from agents.decision_agent import DecisionAgent


class AgentOrchestrator:
    """
    Central coordinator for ResolveAI.

    The orchestrator:
    1. Receives a customer request
    2. Selects the required agents
    3. Executes the selected agents
    4. Sends their results to the Decision Agent
    5. Produces the final resolution
    6. Tracks the workflow state
    """

    def __init__(self, agents: List[BaseAgent] | None = None):
        self.agents: Dict[str, BaseAgent] = {}

        if agents:
            for agent in agents:
                self.register_agent(agent)
        else:
            self.register_agent(MockOrderAgent())
            self.register_agent(MockPolicyAgent())
            self.register_agent(MockInventoryAgent())
            self.register_agent(DecisionAgent())

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent using its name."""
        self.agents[agent.name] = agent

    def get_agent(self, name: str) -> BaseAgent | None:
        """Return a registered agent by name."""
        return self.agents.get(name)

    def select_agents(self, customer_request: str) -> List[str]:
        """
        Decide which agents are required for the request.
        """

        request = customer_request.lower()

        selected_agents: List[str] = []

        # Order-related requests
        if any(
            word in request
            for word in [
                "order",
                "arrived",
                "delivery",
                "delivered",
                "damaged",
                "product",
                "package",
            ]
        ):
            selected_agents.append("order")

        # Policy-related requests
        if any(
            word in request
            for word in [
                "replacement",
                "replace",
                "refund",
                "cancel",
                "return",
                "policy",
            ]
        ):
            selected_agents.append("policy")

        # Inventory-related requests
        if any(
            word in request
            for word in [
                "replacement",
                "replace",
                "inventory",
                "stock",
                "warehouse",
                "available",
                "availability",
            ]
        ):
            selected_agents.append("inventory")

        return selected_agents

    def execute_agents(
        self,
        selected_agents: List[str],
        customer_request: str,
    ) -> Dict[str, Any]:
        """
        Execute all selected agents.
        """

        results: Dict[str, Any] = {}

        task = {
            "customer_request": customer_request,
        }

        for agent_name in selected_agents:
            agent = self.get_agent(agent_name)

            if agent is None:
                results[agent_name] = {
                    "agent": agent_name,
                    "status": "error",
                    "error": f"Agent '{agent_name}' is not registered.",
                }
                continue

            try:
                result = agent.run(task)
                results[agent_name] = result

            except Exception as error:
                results[agent_name] = {
                    "agent": agent_name,
                    "status": "error",
                    "error": str(error),
                }

        return results

    def run(self, customer_request: str) -> Dict[str, Any]:
        """
        Run the complete ResolveAI orchestration workflow.
        """

        state: Dict[str, Any] = {
            "customer_request": customer_request,
            "status": "started",
            "current_step": "understand",
            "attempt": 0,
            "selected_agents": [],
            "agent_results": {},
            "history": [],
            "result": None,
        }

        # ---------------------------------------------------------
        # 1. Understand request
        # ---------------------------------------------------------

        state["history"].append(
            {
                "step": "understand",
                "status": "completed",
            }
        )

        # ---------------------------------------------------------
        # 2. Select agents
        # ---------------------------------------------------------

        selected_agents = self.select_agents(customer_request)

        state["selected_agents"] = selected_agents
        state["current_step"] = "retrieve"

        state["history"].append(
            {
                "step": "retrieve",
                "status": "started",
                "agents": selected_agents,
            }
        )

        # ---------------------------------------------------------
        # 3. Execute agents
        # ---------------------------------------------------------

        agent_results = self.execute_agents(
            selected_agents,
            customer_request,
        )

        state["agent_results"] = agent_results
        state["current_step"] = "decision"

        state["history"].append(
            {
                "step": "retrieve",
                "status": "completed",
                "results": agent_results,
            }
        )

        # ---------------------------------------------------------
        # 4. Decision Agent
        # ---------------------------------------------------------

        state["history"].append(
            {
                "step": "decision",
                "status": "started",
            }
        )

        decision_agent = self.get_agent("decision")

        if decision_agent is None:
            state["result"] = {
                "status": "error",
                "error": "Decision agent is not registered.",
            }

        else:
            try:
                decision_result = decision_agent.run(
                    {
                        "customer_request": customer_request,
                        "agent_results": agent_results,
                    }
                )

                state["result"] = decision_result

            except Exception as error:
                state["result"] = {
                    "agent": "decision",
                    "status": "error",
                    "error": str(error),
                }

        state["history"].append(
            {
                "step": "decision",
                "status": "completed",
                "result": state["result"],
            }
        )

        # ---------------------------------------------------------
        # 5. Complete workflow
        # ---------------------------------------------------------

        state["current_step"] = "completed"
        state["status"] = "completed"

        state["history"].append(
            {
                "step": "completed",
                "status": "completed",
            }
        )

        return state