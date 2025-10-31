
class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        self.patterns = {
            'weather': {
                'patterns': ['weather', 'temperature', 'forecast'],
                'required_args': ['location']
            },
            'news': {
                'patterns': ['news', 'headlines', 'articles'],
                'required_args': ['topic']
            },
            'calendar': {
                'patterns': ['calendar', 'schedule', 'appointment'],
                'required_args': ['date']
            }
        }

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        context_requirements = {'missing_args': []}

        if tool_name in self.patterns:
            tool_patterns = self.patterns[tool_name]
            for pattern in tool_patterns['patterns']:
                if pattern in prompt_lower:
                    for arg in tool_patterns['required_args']:
                        if arg not in arguments:
                            context_requirements['missing_args'].append(arg)
                    break

        return context_requirements
