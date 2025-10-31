from typing import Dict, List, Optional, Any
from openmanus_rl.memory.file_memory import FileMemory
import re

class MemoryStoreModule:
    """Memory storage stage - saves important information."""

    def __init__(self, memory: FileMemory):
        self.memory = memory

    def process(self, text: str, episode: str='', step: int=0) -> Dict[str, Any]:
        """Process memory store stage."""
        store_match = re.search('<memory store>(.*?)</memory store>', text, re.DOTALL)
        if not store_match:
            return {'stored': None}
        content = store_match.group(1).strip()
        self.memory.store_to_file(content, episode, step)
        metadata = f'E:{episode}|S:{step}'
        return {'stored': content, 'metadata': metadata}