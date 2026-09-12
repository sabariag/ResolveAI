from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """
    Base interface for all ResolveAI agents.

    Every agent should:
    1. Receive a task
    2. Process the task
    3. Return a structured result
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task.

        Args:
            task: Input information required by the agent.

        Returns:
            A structured dictionary containing the result.
        """
        pass