from typing import Any, Dict

from agents.base_agent import BaseAgent


class DecisionAgent(BaseAgent):
    """
    Makes a resolution decision using the results
    collected from other agents.
    """

    def __init__(self):
        super().__init__("decision")

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        agent_results = task.get("agent_results", {})

        order_result = agent_results.get("order", {})
        policy_result = agent_results.get("policy", {})
        inventory_result = agent_results.get("inventory", {})

        order_data = order_result.get("data", {})
        policy_data = policy_result.get("data", {})
        inventory_data = inventory_result.get("data", {})

        condition = order_data.get("condition")
        replacement_allowed = policy_data.get(
            "replacement_allowed",
            False,
        )
        inventory_available = inventory_data.get(
            "available",
            False,
        )

        # Decision 1: approve replacement
        if (
            condition == "damaged"
            and replacement_allowed
            and inventory_available
        ):
            return {
                "agent": self.name,
                "status": "success",
                "decision": "APPROVE_REPLACEMENT",
                "reason": (
                    "The product is damaged, replacement is allowed "
                    "by policy, and the product is available in inventory."
                ),
                "action": {
                    "type": "replacement",
                    "product": order_data.get("product"),
                    "order_id": order_data.get("order_id"),
                    "warehouse": inventory_data.get("warehouse"),
                },
            }

        # Decision 2: replacement allowed but product unavailable
        if condition == "damaged" and replacement_allowed:
            return {
                "agent": self.name,
                "status": "success",
                "decision": "REPLACEMENT_UNAVAILABLE",
                "reason": (
                    "The product qualifies for replacement, "
                    "but it is currently unavailable in inventory."
                ),
                "action": {
                    "type": "escalate",
                    "order_id": order_data.get("order_id"),
                },
            }

        # Decision 3: replacement not allowed
        if condition == "damaged" and not replacement_allowed:
            return {
                "agent": self.name,
                "status": "success",
                "decision": "REPLACEMENT_REJECTED",
                "reason": (
                    "The product is damaged, but replacement "
                    "is not allowed by the current policy."
                ),
                "action": {
                    "type": "escalate",
                    "order_id": order_data.get("order_id"),
                },
            }

        # Fallback
        return {
            "agent": self.name,
            "status": "success",
            "decision": "NEEDS_REVIEW",
            "reason": (
                "The available information is not sufficient "
                "to make an automatic resolution."
            ),
            "action": {
                "type": "escalate",
                "order_id": order_data.get("order_id"),
            },
        }