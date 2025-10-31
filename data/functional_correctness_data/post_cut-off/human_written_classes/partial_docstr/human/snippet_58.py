from openmanus_rl.memory.file_memory import FileMemory
from typing import Dict, List, Optional, Any
import re

class ReflectionModule:
    """Reflection stage - analyzes results and queries memory."""

    def __init__(self, memory: FileMemory):
        self.memory = memory

    def process(self, text: str, episode: str='', step: int=0) -> Dict[str, Any]:
        """Process reflection stage with memory queries."""
        reflection_match = re.search('<reflection\\s*>(.*?)</reflection>', text, re.DOTALL | re.IGNORECASE)
        if not reflection_match:
            return {'reflection': None}
        reflection_content = reflection_match.group(1).strip()
        queries = re.findall('<memory query>(.*?)</memory query>', reflection_content, re.DOTALL)
        augmented = text
        for query in queries:
            result = self.memory.query(query.strip())
            augmented = augmented.replace(f'<memory query>{query}</memory query>', f'<memory query>{query}</memory query>\n<memory result>{result}</memory result>', 1)
        clean_reflection = re.sub('<memory query>.*?</memory query>', '', reflection_content, flags=re.DOTALL)
        clean_reflection = re.sub('<memory result>.*?</memory result>', '', clean_reflection, flags=re.DOTALL)
        if clean_reflection:
            self.memory.store_to_file(f'[Reflection] {clean_reflection.strip()}', episode, step)
        return {'reflection': clean_reflection.strip(), 'queries': queries, 'augmented_text': augmented}