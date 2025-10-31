import re
from typing import Any, Dict, List, Pattern, Set


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        # Core intent patterns
        self.patterns: Dict[str, List[Pattern]] = {
            'code_generation': [
                re.compile(
                    r'\b(write|generate|implement|create|produce)\b.*\b(code|function|class|script|module|program)\b', re.I | re.S),
                re.compile(r'```', re.I),
            ],
            'bug_fix': [
                re.compile(
                    r'\b(fix|debug|resolve|diagnose)\b.*\b(bug|error|issue|exception|traceback)\b', re.I),
            ],
            'unit_test': [
                re.compile(
                    r'\b(write|create|generate)\b.*\b(unit\s*tests?|tests?|pytest|unittest)\b', re.I),
            ],
            'refactor': [
                re.compile(
                    r'\b(refactor|clean\s*up|improve|restructure)\b.*\b(code|function|module|class)\b', re.I),
            ],
            'summarize': [
                re.compile(r'\b(summarize|summary|tl;dr)\b', re.I),
            ],
            'translate': [
                re.compile(r'\b(translate|transliterate)\b', re.I),
            ],
            'sentiment': [
                re.compile(r'\b(sentiment|tone|emotion|polarity)\b', re.I),
            ],
            'extract': [
                re.compile(
                    r'\b(extract|pull|parse|identify)\b.*\b(entity|entities|names|emails|urls|dates|numbers|data)\b', re.I),
            ],
            'web_search': [
                re.compile(
                    r'\b(search|look\s*up|find|google)\b.*\b(web|internet|online|site|page)\b', re.I),
                re.compile(r'https?://', re.I),
            ],
            'data_analysis': [
                re.compile(
                    r'\b(analy[sz]e|analysis|analytics|statistical|regression|correlation|cluster|model)\b', re.I),
            ],
            'math': [
                re.compile(
                    r'\b(calculate|compute|solve|integrate|differentiate|sum|average|derivative|integral|equation)\b', re.I),
            ],
            'scheduling': [
                re.compile(
                    r'\b(schedule|meeting|calendar|appoint\w*)\b', re.I),
            ],
            'email_drafting': [
                re.compile(
                    r'\b(draft|write|compose)\b.*\b(email|mail)\b', re.I),
            ],
            'sql': [
                re.compile(r'```sql', re.I),
                re.compile(
                    r'\b(select|insert|update|delete)\b.*\b(from|into)\b', re.I | re.S),
            ],
            'shell': [
                re.compile(
                    r'\b(run|execute)\b.*\b(command|shell|bash|terminal)\b', re.I),
                re.compile(r'\b(ls|grep|cat|cd|mkdir|curl|wget)\b', re.I),
                re.compile(r'```(?:bash|sh|shell)', re.I),
            ],
            'file_ops': [
                re.compile(
                    r'\b(read|write|open|load|save|rename|delete|remove|copy|move)\b.*\b(file|path|directory|folder)\b', re.I),
            ],
            'api_call': [
                re.compile(
                    r'\b(call|hit|request|invoke|fetch)\b.*\b(api|endpoint|http)\b', re.I),
                re.compile(r'\bGET|POST|PUT|PATCH|DELETE\b', re.I),
            ],
            'configuration': [
                re.compile(
                    r'\b(configure|configuration|settings|set\s*up|setup)\b', re.I),
            ],
            'visualization': [
                re.compile(r'\b(plot|chart|graph|visuali[sz]e)\b', re.I),
            ],
            'compare': [
                re.compile(r'\b(compare|comparison|versus|vs\.)\b', re.I),
            ],
            'proofreading': [
                re.compile(
                    r'\b(proofread|grammar|spell|correct|copyedit)\b', re.I),
            ],
            'legal': [
                re.compile(
                    r'\b(contract|agreement|clause|statute|legal|law)\b', re.I),
            ],
        }

        # Entity extractors
        self.entity_patterns: Dict[str, Pattern] = {
            'urls': re.compile(r'https?://[^\s)>\]}\'"]+', re.I),
            'emails': re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b'),
            'dates': re.compile(r'\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s*\d{2,4})\b', re.I),
            'times': re.compile(r'\b\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)?\b'),
            'currencies': re.compile(r'[$€£]\s?\d{1,3}(?:[,\s]\d{3})*(?:\.\d+)?'),
            'percentages': re.compile(r'\b\d+(?:\.\d+)?\s?%|\bpercent\b', re.I),
            'file_paths': re.compile(r'(?:(?:[A-Za-z]:\\|/)[^ \t\n\r\f\v\'"]+)', re.I),
            'ip_addresses': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
            'issue_ids': re.compile(r'\b[A-Z]{2,10}-\d+\b'),
            'code_fences': re.compile(r'```(\w+)?', re.I),
            'json_like': re.compile(r'\{[^{}]{0,500}:[^{}]{0,500}\}'),
            'numbers': re.compile(r'\b\d+(?:\.\d+)?\b'),
        }

        # Map patterns to high-level context flags
        self.context_map: Dict[str, Dict[str, bool]] = {
            'web_search': {'needs_web': True, 'needs_internet': True},
            'api_call': {'needs_internet': True, 'needs_api': True},
            'file_ops': {'needs_filesystem': True},
            'shell': {'needs_shell': True, 'needs_code_execution': True},
            'sql': {'needs_database': True, 'needs_code_execution': True},
            'code_generation': {'needs_code_execution': True},
            'bug_fix': {'needs_code_execution': True},
            'unit_test': {'needs_code_execution': True},
            'refactor': {'needs_code_execution': True},
            'data_analysis': {'needs_code_execution': True, 'needs_data': True},
            'math': {'needs_code_execution': True},
            'visualization': {'needs_code_execution': True, 'needs_plotting': True},
            'email_drafting': {'needs_email': True},
            'scheduling': {'needs_calendar': True},
        }

        # Tool alignment keywords by category
        self.tool_keywords: Dict[str, List[str]] = {
            'web_search': ['search', 'browser', 'browse', 'web', 'serp'],
            'code_executor': ['python', 'execute', 'runner', 'notebook', 'jupyter', 'sandbox'],
            'filesystem': ['file', 'fs', 'filesystem', 'path', 'storage'],
            'sql': ['sql', 'database', 'db', 'sqlite', 'postgres', 'mysql'],
            'bash': ['shell', 'bash', 'terminal', 'sh'],
            'http': ['api', 'http', 'curl', 'request', 'fetch'],
            'email': ['email', 'gmail', 'outlook', 'smtp'],
            'calendar': ['calendar', 'schedule'],
            'viz': ['plot', 'chart', 'graph', 'viz'],
            'nlp': ['summarize', 'translate', 'extract', 'nlp', 'spacy'],
        }

        # Map pattern -> tool category for alignment
        self.pattern_tool_category: Dict[str, str] = {
            'web_search': 'web_search',
            'api_call': 'http',
            'file_ops': 'filesystem',
            'shell': 'bash',
            'sql': 'sql',
            'code_generation': 'code_executor',
            'bug_fix': 'code_executor',
            'unit_test': 'code_executor',
            'refactor': 'code_executor',
            'data_analysis': 'code_executor',
            'math': 'code_executor',
            'visualization': 'viz',
            'email_drafting': 'email',
            'scheduling': 'calendar',
            'summarize': 'nlp',
            'translate': 'nlp',
            'extract': 'nlp',
            'sentiment': 'nlp',
            'proofreading': 'nlp',
        }

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        text = prompt or ''
        tool = (tool_name or '').lower()
        args = arguments or {}

        pattern_results: List[Dict[str, Any]] = []
        evidence_total = 0

        for pname, regs in self.patterns.items():
            matches_info: List[Dict[str, Any]] = []
            evidence = 0
            for reg in regs:
                for m in reg.finditer(text):
                    snippet_start = max(0, m.start() - 32)
                    snippet_end = min(len(text), m.end() + 32)
                    matches_info.append({
                        'span': [m.start(), m.end()],
                        'snippet': text[snippet_start:snippet_end]
                    })
                    evidence += 1
                    evidence_total += 1
            if evidence > 0:
                base_conf = min(1.0, 0.4 + 0.18 * min(5, evidence))
                # Boost if tool aligns with pattern category
                if self._tool_aligns_with_pattern(tool, pname):
                    base_conf = min(1.0, base_conf + 0.2)
                # Boost if arguments contain related hints
                base_conf = self._boost_by_arguments(base_conf, pname, args)
                pattern_results.append({
                    'name': pname,
                    'matches': matches_info,
                    'confidence': round(base_conf, 3)
                })

        entities = self._extract_entities(text)
        context = self._derive_context(pattern_results, entities, args)

        entity_count = sum(len(v) for v in entities.values())
        top_conf = max([p['confidence'] for p in pattern_results], default=0.0)
        overall_conf = min(1.0, top_conf + (0.05 * min(10, entity_count)
                                            ) + (0.05 if evidence_total > 2 else 0.0))

        tool_alignment = {
            'tool_name': tool_name,
            'alignment': self._tool_overall_alignment(tool, pattern_results),
            'suggested_tools': self._suggest_tools(pattern_results, tool),
        }

        return {
            'patterns': sorted(pattern_results, key=lambda x: x['confidence'], reverse=True),
            'entities': entities,
            'context': context,
            'confidence': round(overall_conf, 3),
            'tool_alignment': tool_alignment,
        }

    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        results: Dict[str, List[str]] = {}
        for name, pattern in self.entity_patterns.items():
            values: Set[str] = set()
            for m in pattern.finditer(text):
                if name == 'code_fences':
                    lang = (m.group(1) or '').strip()
                    if lang:
                        values.add(lang.lower())
                else:
                    values.add(m.group(0))
            if values:
                results[name] = sorted(values)
        return results

    def _derive_context(self, patterns: List[Dict[str, Any]], entities: Dict[str, List[str]], args: Dict[str, Any]) -> Dict[str, bool]:
        ctx_flags: Dict[str, bool] = {
            'needs_web': False,
            'needs_internet': False,
            'needs_api': False,
            'needs_filesystem': False,
            'needs_code_execution': False,
            'needs_database': False,
            'needs_shell': False,
            'needs_email': False,
            'needs_calendar': False,
            'needs_data': False,
            'needs_plotting': False,
        }
        # From patterns
        for p in patterns:
            mapping = self.context_map.get(p['name'], {})
            for k, v in mapping.items():
                if v:
                    ctx_flags[k] = True

        # From entities
        if entities.get('urls'):
            ctx_flags['needs_internet'] = True
            ctx_flags['needs_web'] = True
        if entities.get('file_paths'):
            ctx_flags['needs_filesystem'] = True
        if entities.get('code_fences'):
            ctx_flags['needs_code_execution'] = True
        if 'json_like' in entities:
            ctx_flags['needs_data'] = True

        # From arguments
        arg_keys = {str(k).lower()
                    for k in (args.keys() if isinstance(args, dict) else [])}
        arg_text = ' '.join([str(v) for v in args.values()]
                            ) if isinstance(args, dict) else ''
        if any(k in arg_keys for k in ['url', 'urls', 'endpoint', 'http', 'query']):
            ctx_flags['needs_internet'] = True
        if any(k in arg_keys for k in ['file', 'filepath', 'path', 'directory']):
            ctx_flags['needs_filesystem'] = True
        if any(k in arg_keys for k in ['sql', 'database', 'db']):
            ctx_flags['needs_database'] = True
        if any(k in arg_keys for k in ['command', 'bash', 'shell']):
            ctx_flags['needs_shell'] = True
        if re.search(self.patterns['sql'][0], arg_text) or re.search(self.patterns['sql'][1], arg_text):
            ctx_flags['needs_database'] = True

        return ctx_flags

    def _tool_aligns_with_pattern(self, tool: str, pattern_name: str) -> bool:
        category = self.pattern_tool_category.get(pattern_name)
        if not category:
            return False
        keywords = self.tool_keywords.get(category, [])
        return any(k in tool for k in keywords)

    def _tool_overall_alignment(self, tool: str, patterns: List[Dict[str, Any]]) -> float:
        if not tool:
            return 0.0
        if not patterns:
            return 0.0
        aligned_scores = []
        for p in patterns:
            aligned = self._tool_aligns_with_pattern(tool, p['name'])
            aligned_scores.append(p['confidence'] if aligned else 0.0)
        if not aligned_scores:
            return 0.0
        score = sum(aligned_scores) / max(1, len(patterns))
        return round(min(1.0, score), 3)

    def _boost_by_arguments(self, conf: float, pattern_name: str, args: Dict[str, Any]) -> float:
        if not isinstance(args, dict):
            return conf
        flat = ' '.join([f'{k} {v}' for k, v in args.items()]).lower()
        boosts = {
            'web_search': ['url', 'query', 'search'],
            'api_call': ['api', 'endpoint', 'authorization', 'token', 'header'],
            'file_ops': ['file', 'path', 'directory'],
            'sql': ['sql', 'select', 'from', 'where', 'database', 'db'],
            'shell': ['bash', 'shell', 'command'],
            'visualization': ['plot', 'chart', 'figure'],
            'data_analysis': ['data', 'csv', 'dataset', 'pandas'],
        }
        for kw in boosts.get(pattern_name, []):
            if kw in flat:
                conf = min(1.0, conf + 0.1)
        return conf

    def _suggest_tools(self, patterns: List[Dict[str, Any]], current_tool: str) -> List[str]:
        suggestions: List[str] = []
        seen: Set[str] = set()
        priority = sorted(
            patterns, key=lambda p: p['confidence'], reverse=True)[:5]
        mapping = {
            'web_search': 'web_search',
            'api_call': 'http_client',
            'file_ops': 'filesystem',
            'shell': 'bash',
            'sql': 'sql_executor',
            'code_generation': 'code_executor',
            'bug_fix': 'code_executor',
            'unit_test': 'code_executor',
            'refactor': 'code_executor',
            'data_analysis': 'python_pandas',
            'math': 'python_executor',
            'visualization': 'python_matplotlib',
            'email_drafting': 'email_client',
            'scheduling': 'calendar',
            'summarize': 'nlp_summarizer',
            'translate': 'nlp_translator',
            'extract': 'nlp_ner',
            'sentiment': 'nlp_sentiment',
            'proofreading': 'nlp_proofreader',
        }
        ct = (current_tool or '').lower()
        for p in priority:
            tool = mapping.get(p['name'])
            if tool and tool not in seen and tool not in ct:
                suggestions.append(tool)
                seen.add(tool)
        return suggestions
