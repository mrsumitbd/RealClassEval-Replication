from openmanus_rl.memory.file_memory import FileMemory
import re
from typing import Dict, List, Optional, Any

class PlanningModule:
    """Planning stage - reads from memory, outputs plan."""

    def __init__(self, memory: FileMemory):
        self.memory = memory

    def process(self, text: str) -> Dict[str, Any]:
        """Process planning stage with memory queries."""
        plan_match = re.search('<plan>(.*?)</plan>', text, re.DOTALL)
        if not plan_match:
            return {'plan': None, 'augmented_text': text}
        plan_content = plan_match.group(1).strip()
        queries = re.findall('<memory query>(.*?)</memory query>', plan_content, re.DOTALL)
        augmented = text
        for query in queries:
            result = self.memory.query(query.strip())
            augmented = augmented.replace(f'<memory query>{query}</memory query>', f'<memory query>{query}</memory query>\n<memory result>{result}</memory result>', 1)
        clean_plan = re.sub('<memory query>.*?</memory query>', '', plan_content, flags=re.DOTALL)
        clean_plan = re.sub('<memory result>.*?</memory result>', '', clean_plan, flags=re.DOTALL)
        return {'plan': clean_plan.strip(), 'queries': queries, 'augmented_text': augmented}