from typing import Any, Dict

from agents.base_agent import BaseAgent
from tools.order_tools import get_order


class MockOrderAgent(BaseAgent):

    def __init__(self):
        super().__init__("order")

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        order_id = task.get("order_id", "ORD-1001")

        order = get_order(order_id)

        if order is None:
            return {
                "agent": self.name,
                "status": "failed",
                "error": "Order " + order_id + " not found"
            }

        return {
            "agent": self.name,
            "status": "success",
            "data": {
                "order_id": order_id,
                "product": order["product"],
                "condition": order["condition"]
            }
        }


class MockPolicyAgent(BaseAgent):

    def __init__(self):
        super().__init__("policy")

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        from tools.policy_tools import (
            check_replacement_policy,
            check_refund_policy,
            check_cancellation_policy,
        )

        order_status = task.get(
            "order_status",
            "delivered"
        )

        condition = task.get(
            "condition",
            "damaged"
        )

        replacement_result = check_replacement_policy(
            condition
        )

        refund_result = check_refund_policy(
            order_status
        )

        cancellation_result = check_cancellation_policy(
            order_status
        )

        return {
            "agent": self.name,
            "status": "success",
            "data": {
                "replacement_allowed":
                    replacement_result["allowed"],
                "refund_allowed":
                    refund_result["allowed"],
                "cancellation_allowed":
                    cancellation_result["allowed"],
            }
        }


class MockInventoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("inventory")

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "agent": self.name,
            "status": "success",
            "data": {
                "product": "Headphones",
                "available": True,
                "warehouse": "WH-01"
            }
        }