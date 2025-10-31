from pathlib import Path
from dataclasses import dataclass

@dataclass
class BaseTask:
    """Base class for evaluation tasks."""
    task_instruction_path: Path
    task_verification_path: Path
    service: str
    category_id: str
    task_id: str

    @property
    def name(self) -> str:
        """Return the task name using '__' separator format: 'category_id__task_id'."""
        return f'{self.category_id}__{self.task_id}'

    def get_task_instruction(self) -> str:
        """Return the full text content of the task instruction file."""
        if not self.task_instruction_path.exists():
            raise FileNotFoundError(f'Task instruction file not found: {self.task_instruction_path}')
        return self.task_instruction_path.read_text(encoding='utf-8')