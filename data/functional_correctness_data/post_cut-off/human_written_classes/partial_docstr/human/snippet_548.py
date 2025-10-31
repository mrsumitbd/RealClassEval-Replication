from typing import Any, Dict, List, Optional, Union
from langchain_core.tools import BaseTool
import copy
from typing import Dict, List

class Task:
    """Task to be executed."""

    def __init__(self, task: str, id: int, dep: List[int], args: Dict, tool: BaseTool):
        self.task = task
        self.id = id
        self.dep = dep
        self.args = args
        self.tool = tool
        self.status = 'pending'
        self.message = ''
        self.result = ''

    def __str__(self) -> str:
        return f'{self.task}({self.args})'

    def save_product(self) -> None:
        """Save text-based products to result field."""
        if hasattr(self, 'product'):
            self.result = str(self.product)

    def completed(self) -> bool:
        return self.status == 'completed'

    def failed(self) -> bool:
        return self.status == 'failed'

    def pending(self) -> bool:
        return self.status == 'pending'

    def run(self) -> str:
        """Execute the task using the associated tool."""
        try:
            new_args = copy.deepcopy(self.args)
            result = self.tool(**new_args)
            if isinstance(result, str):
                self.result = result
            else:
                self.product = result
                self.save_product()
        except Exception as e:
            self.status = 'failed'
            self.message = str(e)
            return self.message
        self.status = 'completed'
        return self.result