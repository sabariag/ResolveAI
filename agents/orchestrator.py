from typing import Any, Dict, List

from agents.base_agent import BaseAgent
from agents.mock_agents import (
    MockOrderAgent,
    MockPolicyAgent,
    MockInventoryAgent,
)
from agents.decision_agent import DecisionAgent

from tools.action_tools import (
    execute_replacement,
    execute_refund,
    execute_cancellation,
    execute_escalation,
)


class AgentOrchestrator:
    """
    Central coordinator for ResolveAI.

    The orchestrator:
    1. Receives a customer request
    2. Selects the required agents
    3. Executes the selected agents
    4. Sends their results to the Decision Agent
    5. Executes the recommended action
    6. Verifies the action
    7. Produces the final resolution
    8. Tracks the workflow state
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
        Select the minimum set of agents required to understand
        and resolve the customer request.
        """

        request = customer_request.lower().strip()
        selected_agents: List[str] = []

        inventory_keywords = [
            "stock",
            "inventory",
            "warehouse",
            "available",
            "availability",
            "replacement",
            "replace",
        ]

        policy_keywords = [
            "replacement",
            "replace",
            "refund",
            "return",
            "cancel",
            "cancellation",
            "policy",
        ]

        order_keywords = [
            "order",
            "arrived",
            "delivery",
            "delivered",
            "damaged",
            "package",
        ]

        is_inventory_request = any(
            word in request for word in inventory_keywords
        )

        is_policy_request = any(
            word in request for word in policy_keywords
        )

        is_order_request = any(
            word in request for word in order_keywords
        )

        if (
            is_inventory_request
            and not is_order_request
            and not is_policy_request
        ):
            selected_agents.append("inventory")
            return selected_agents

        if is_order_request:
            selected_agents.append("order")

        if is_policy_request:
            selected_agents.append("policy")

        if is_inventory_request:
            selected_agents.append("inventory")

        return selected_agents

    def execute_agents(
        self,
        selected_agents: List[str],
        customer_request: str,
    ) -> Dict[str, Any]:
        """Execute selected agents with one automatic retry."""

        results: Dict[str, Any] = {}

        task = {
           "customer_request": customer_request,
           "order_status": "delivered",
           "condition": "damaged",
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

            # -------------------------------------------------
            # FIRST ATTEMPT
            # -------------------------------------------------
            try:
                result = agent.run(task)

            except Exception as error:
                result = {
                    "agent": agent_name,
                    "status": "error",
                    "error": str(error),
                }

            # -------------------------------------------------
            # RETRY IF FIRST ATTEMPT FAILED
            # -------------------------------------------------
            if result.get("status") != "success":

                print(
                    f"\n⚠️ Agent '{agent_name}' failed. "
                    "Retrying..."
                )

                try:
                    retry_result = agent.run(task)

                    if retry_result.get("status") == "success":
                        retry_result["retry"] = True
                        retry_result["attempt"] = 2
                        results[agent_name] = retry_result
                        continue

                    retry_result["retry"] = True
                    retry_result["attempt"] = 2
                    results[agent_name] = retry_result

                except Exception as error:
                    results[agent_name] = {
                        "agent": agent_name,
                        "status": "error",
                        "error": str(error),
                        "retry": True,
                        "attempt": 2,
                    }

            else:
                result["retry"] = False
                result["attempt"] = 1
                results[agent_name] = result

        return results

    def execute_action(
        self,
        decision_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute the action recommended by the Decision Agent."""

        if decision_result.get("status") != "success":
            return {
                "success": False,
                "message": "Decision was not successful",
            }

        action = decision_result.get("action")

        if not action:
            return {
                "success": True,
                "action":"information",
                "message":decision_result.get(
                    "reason","information retrieved successfully",
                ),
                "data": decision_result.get("data", {}),
            }

        action_type = action.get("type")

        if action_type == "replacement":
         return execute_replacement(
           order_id=action.get("order_id"),
           product=action.get("product"),
           warehouse=action.get("warehouse"),
         )

        if action_type == "escalate":
         return execute_escalation(
           order_id=action.get("order_id"),
         )

        if action_type == "refund":
            return execute_refund(
                order_id=action.get("order_id"),
                amount=action.get("amount", 0),
            )

        if action_type == "cancellation":
            return execute_cancellation(
                order_id=action.get("order_id"),
            )

        return {
            "success": False,
            "message": f"Unsupported action type: {action_type}",
        }

    def verify_action(
        self,
        action_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Verify whether the executed action was successful."""

        if action_result.get("success") is True:
            return {
                "verified": True,
                "status": "success",
                "message": action_result.get(
                    "message",
                    "Action verified successfully",
                ),
            }

        return {
            "verified": False,
            "status": "failed",
            "message": action_result.get(
                "message",
                "Action verification failed",
            ),
        }

    def run(self, customer_request: str) -> Dict[str, Any]:
        """Run the complete ResolveAI orchestration workflow."""

        state: Dict[str, Any] = {
            "customer_request": customer_request,
            "status": "started",
            "current_step": "understand",
            "attempt": 0,
            "selected_agents": [],
            "agent_results": {},
            "history": [],
            "result": None,
            "action_result": None,
            "verification": None,
        }

        # 1. Understand request
        state["history"].append(
            {
                "step": "understand",
                "status": "completed",
            }
        )

        # 2. Select agents
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

        # 3. Execute agents
        agent_results = self.execute_agents(
            selected_agents,
            customer_request,
        )

        state["agent_results"] = agent_results
                # Record retry information in workflow history
        for agent_name, result in agent_results.items():
            if result.get("retry") is True:
                state["history"].append(
                    {
                        "step": "retry",
                        "agent": agent_name,
                        "attempt": result.get("attempt", 2),
                        "status": result.get("status"),
                    }
                )
        state["current_step"] = "decision"

        state["history"].append(
            {
                "step": "retrieve",
                "status": "completed",
                "results": agent_results,
            }
        )

        # 4. Decision Agent
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

        # 5. Execute Action
        state["current_step"] = "execute_action"

        state["history"].append(
            {
                "step": "execute_action",
                "status": "started",
            }
        )

        action_result = self.execute_action(
            state["result"]
        )

        state["action_result"] = action_result

        state["history"].append(
            {
                "step": "execute_action",
                "status": "completed",
                "result": action_result,
            }
        )

        # 6. Verify Action
        state["current_step"] = "verify"

        state["history"].append(
            {
                "step": "verify",
                "status": "started",
            }
        )

        verification = self.verify_action(
            action_result
        )

        state["verification"] = verification

        state["history"].append(
            {
                "step": "verify",
                "status": "completed",
                "result": verification,
            }
        )

        # 7. Complete workflow
        if verification["verified"]:
            state["status"] = "completed"
            state["current_step"] = "completed"
        else:
            state["status"] = "failed"
            state["current_step"] = "failed"

        state["history"].append(
            {
                "step": state["current_step"],
                "status": state["status"],
            }
        )

        return state
