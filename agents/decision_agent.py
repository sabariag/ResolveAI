from typing import Any, Dict

from agents.base_agent import BaseAgent


class DecisionAgent(BaseAgent):
    """
    Makes a resolution decision using:
    - customer request
    - order information
    - policy information
    - inventory information
    """

    def __init__(self):
        super().__init__("decision")

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        customer_request = task.get("customer_request", "").lower()

        agent_results = task.get("agent_results", {})
                # ---------------------------------------------------------
        # PHASE 4: AGENT RESULT VALIDATION
        # ---------------------------------------------------------
        for agent_name, result in agent_results.items():
            if result.get("status") != "success":
                return {
                    "agent": self.name,
                    "status": "success",
                    "decision": "NEEDS_REVIEW",
                    "reason": (
                        f"The {agent_name} agent did not complete "
                        "successfully, so an automatic decision "
                        "cannot be made safely."
                    ),
                    "action": {
                        "type": "escalate",
                        "order_id": task.get("order_id"),
                    },
                    "failed_agent": agent_name,
                }

        order_result = agent_results.get("order", {})
        policy_result = agent_results.get("policy", {})
        inventory_result = agent_results.get("inventory", {})

        order_data = order_result.get("data", {})
        policy_data = policy_result.get("data", {})
        inventory_data = inventory_result.get("data", {})

        order_id = order_data.get("order_id")
        product = order_data.get("product")
        condition = order_data.get("condition")

        replacement_allowed = policy_data.get(
            "replacement_allowed",
            False,
        )

        refund_allowed = policy_data.get(
            "refund_allowed",
            False,
        )

        cancellation_allowed = policy_data.get(
            "cancellation_allowed",
            True,
        )

        inventory_available = inventory_data.get(
            "available",
            False,
        )

        warehouse = inventory_data.get("warehouse")

        # ---------------------------------------------------------
        # 1. REFUND REQUEST
        # ---------------------------------------------------------
        if "refund" in customer_request:
            if refund_allowed:
                return {
                    "agent": self.name,
                    "status": "success",
                    "decision": "APPROVE_REFUND",
                    "reason": (
                        "Refund is allowed by the current policy."
                    ),
                    "action": {
                        "type": "refund",
                        "order_id": order_id,
                        "amount": order_data.get("amount", 1999),
                    },
                }

            return {
                "agent": self.name,
                "status": "success",
                "decision": "REFUND_REJECTED",
                "reason": (
                    "Refund is not allowed by the current policy."
                ),
                "action": {
                    "type": "escalate",
                    "order_id": order_id,
                },
            }

        # ---------------------------------------------------------
        # 2. CANCELLATION REQUEST
        # ---------------------------------------------------------
        if "cancel" in customer_request or "cancellation" in customer_request:
            if cancellation_allowed:
                return {
                    "agent": self.name,
                    "status": "success",
                    "decision": "APPROVE_CANCELLATION",
                    "reason": (
                        "The order can be cancelled according "
                        "to the current policy."
                    ),
                    "action": {
                        "type": "cancellation",
                        "order_id": order_id,
                    },
                }

            return {
                "agent": self.name,
                "status": "success",
                "decision": "CANCELLATION_REJECTED",
                "reason": (
                    "Order cancellation is not allowed "
                    "by the current policy."
                ),
                "action": {
                    "type": "escalate",
                    "order_id": order_id,
                },
            }

        # ---------------------------------------------------------
        # 3. INVENTORY / STOCK REQUEST
        # ---------------------------------------------------------
        if (
            "stock" in customer_request
            or "inventory" in customer_request
            or "available" in customer_request
        ):
            if inventory_result.get("status") == "success":
                return {
                    "agent": self.name,
                    "status": "success",
                    "decision": "INVENTORY_INFORMATION",
                    "reason": (
                        "Inventory information was successfully "
                        "retrieved."
                    ),
                    "action": None,
                    "data": {
                        "product": product
                        or inventory_data.get("product"),
                        "available": inventory_available,
                        "warehouse": warehouse,
                    },
                }

        # ---------------------------------------------------------
        # 4. WAREHOUSE REQUEST
        # ---------------------------------------------------------
        if "warehouse" in customer_request:
            if inventory_result.get("status") == "success":
                return {
                    "agent": self.name,
                    "status": "success",
                    "decision": "WAREHOUSE_INFORMATION",
                    "reason": (
                        "Warehouse information was successfully "
                        "retrieved."
                    ),
                    "action": None,
                    "data": {
                        "product": product
                        or inventory_data.get("product"),
                        "warehouse": warehouse,
                        "available": inventory_available,
                    },
                }

        # ---------------------------------------------------------
        # 5. REPLACEMENT REQUEST
        # ---------------------------------------------------------
        if (
            "replacement" in customer_request
            or "replace" in customer_request
            or condition == "damaged"
        ):
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
                        "The product is damaged, replacement is "
                        "allowed by policy, and the product is "
                        "available in inventory."
                    ),
                    "action": {
                        "type": "replacement",
                        "product": product,
                        "order_id": order_id,
                        "warehouse": warehouse,
                    },
                }

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
                        "order_id": order_id,
                    },
                }

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
                        "order_id": order_id,
                    },
                }

        # ---------------------------------------------------------
        # 6. FALLBACK
        # ---------------------------------------------------------
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
                "order_id": order_id,
            },
        }