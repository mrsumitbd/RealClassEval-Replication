from typing import Dict, List, Optional, Any
from openmanus_rl.memory.file_memory import FileMemory
import re

class ModularStageProcessor:
    """Main processor that orchestrates all stages."""

    def __init__(self, memory_file: str='memory.md'):
        self.memory = FileMemory(memory_file)
        self.planning = PlanningModule(self.memory)
        self.action = ActionModule(self.memory)
        self.memory_store = MemoryStoreModule(self.memory)
        self.reflection = ReflectionModule(self.memory)

    def register_tool(self, name: str, func):
        """Register tool in action module."""
        self.action.register_tool(name, func)

    def query_memory(self, query: str, top_k: int=3) -> str:
        """Query memory - delegate to memory module."""
        return self.memory.query(query, top_k)

    def store_memory(self, content: str, episode: str='', step: int=0):
        """Store memory - delegate to memory module."""
        self.memory.store_to_file(content, episode, step)

    def process_response(self, text: str, episode: str='', step: int=0) -> Dict[str, Any]:
        """Process all stages in sequence."""
        results = {'original': text, 'augmented': text}
        plan_result = self.planning.process(results['augmented'])
        results['plan'] = plan_result
        if 'augmented_text' in plan_result:
            results['augmented'] = plan_result['augmented_text']
        action_result = self.action.process(results['augmented'])
        results['action'] = action_result
        if 'augmented_text' in action_result:
            results['augmented'] = action_result['augmented_text']
        store_result = self.memory_store.process(results['augmented'], episode, step)
        results['memory_store'] = store_result
        reflection_result = self.reflection.process(results['augmented'], episode, step)
        results['reflection'] = reflection_result
        if 'augmented_text' in reflection_result:
            results['augmented'] = reflection_result['augmented_text']
        results['env_action'] = action_result.get('for_env', '')
        return results

    def parse_simple(self, text: str) -> Dict[str, Optional[str]]:
        """Simple parsing for all tags (utility function)."""
        tags = ['plan', 'action', 'memory store', 'reflection', 'think']
        result = {}
        for tag in tags:
            tag_pattern = tag.replace(' ', '\\s*')
            pattern = f'<{tag_pattern}>(.*?)</{tag_pattern}>'
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            content = match.group(1).strip() if match else None
            if tag == 'action' and content:
                if 'action_choice:' in content:
                    parts = content.split('action_choice:')
                    if len(parts) > 1:
                        action = parts[1].split('\n')[0].strip()
                        action = action.strip('\'"')
                        content = action
                else:
                    content = content.split('\n')[0].strip().strip('\'"')
            result[tag.replace(' ', '_')] = content
        return result