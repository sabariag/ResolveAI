from typing import Any, Dict

from agents.base_agent import BaseAgent


class MockOrderAgent(BaseAgent):
    def __init__(self):
        super().__init__("order")

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "agent": self.name,
            "status": "success",
            "data": {
                "order_id": "ORD-1001",
                "product": "Headphones",
                "condition": "damaged",
            },
        }


class MockPolicyAgent(BaseAgent):
    def __init__(self):
        super().__init__("policy")

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "agent": self.name,
            "status": "success",
            "data": {
                "replacement_allowed": True,
                "refund_allowed": True,
            },
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
                "warehouse": "WH-01",
            },
        }