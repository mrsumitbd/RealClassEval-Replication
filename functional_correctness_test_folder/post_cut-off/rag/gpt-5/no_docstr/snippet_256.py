from typing import Any, Dict, List, Pattern, Tuple, Optional
import re


class PromptPatternMatcher:
    """Analyzes prompts to determine context requirements."""

    def __init__(self):
        """Initialize pattern matchers."""
        self._pattern_specs: Dict[str, List[Tuple[str, Pattern]]] = {
            'web_search': [
                ('search', re.compile(
                    r'\b(search|look\s*up|find\s+(info|information|details)|google|bing|duckduckgo)\b', re.I)),
                ('latest', re.compile(
                    r'\b(latest|up[-\s]*to[-\s]*date|current\s+(news|events|prices|rates))\b', re.I)),
                ('on_the_web', re.compile(r'\b(on|from)\s+the\s+web\b', re.I)),
                ('check_online', re.compile(
                    r'\b(check|verify)\s+(online|on\s+the\s+internet)\b', re.I)),
                ('url_present', re.compile(r'https?://\S+', re.I)),
            ],
            'code_gen': [
                ('write_code', re.compile(
                    r'\b(write|generate|implement|create)\s+(some\s+)?(sample\s+)?(code|function|class|script|module)\b', re.I)),
                ('example_in_lang', re.compile(
                    r'\b(example|snippet)\s+in\s+(python|javascript|typescript|java|c\+\+|c#|go|rust|ruby|php|kotlin|swift|r|matlab|sql|bash|shell|powershell)\b', re.I)),
                ('code_fence', re.compile(r'```(\w+)?[\s\S]*?```', re.I)),
            ],
            'code_debug': [
                ('fix_bug', re.compile(
                    r'\b(fix|resolve|debug)\b.*\b(bug|issue|problem|error)\b', re.I)),
                ('traceback', re.compile(
                    r'\b(traceback|stack\s*trace|exception|segfault|assertion\s*failed)\b', re.I)),
                ('fails', re.compile(
                    r'\b(failing|does\s*not\s*work|not\s*working|unexpected\s+behavior)\b', re.I)),
            ],
            'summarize': [
                ('summarize', re.compile(
                    r'\b(summarize|summary|tl;dr|condense|brief\s+overview)\b', re.I)),
            ],
            'translate': [
                ('translate', re.compile(r'\btranslate\b', re.I)),
                ('to_language', re.compile(
                    r'\b(to|into)\s+(french|spanish|german|italian|portuguese|japanese|chinese|korean|russian|arabic|hindi)\b', re.I)),
            ],
            'sentiment': [
                ('sentiment', re.compile(
                    r'\b(sentiment|tone|emotion|positive|negative|neutral)\b', re.I)),
            ],
            'classify': [
                ('classify', re.compile(r'\b(classify|categorize|tag|label)\b', re.I)),
            ],
            'math': [
                ('calculate', re.compile(
                    r'\b(calculate|compute|evaluate|sum|difference|product|quotient|percentage|probability)\b', re.I)),
                ('expression', re.compile(
                    r'\b\d+(\.\d+)?\s*([+\-*/^%]|plus|minus|times|over)\s*\d+(\.\d+)?\b', re.I)),
                ('advanced', re.compile(
                    r'\b(derivative|integral|limit|matrix|vector|algebra|calculus)\b', re.I)),
            ],
            'date_time': [
                ('temporal', re.compile(
                    r'\b(today|now|current\s*time|current\s*date|time\s*now|day\s*of\s*week|what\s*day\s*is\s*it)\b', re.I)),
                ('calendar', re.compile(
                    r'\b(calendar|schedule|deadline|due\s*date)\b', re.I)),
                ('explicit_date', re.compile(
                    r'\b(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})\b', re.I)),
                ('month_name', re.compile(
                    r'\b(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(t(ember)?)?|oct(ober)?|nov(ember)?|dec(ember)?)\b', re.I | re.IGNORECASE)),
            ],
            'location': [
                ('near_me', re.compile(r'\b(near\s*me|nearby|closest|nearest)\b', re.I)),
                ('where_is', re.compile(
                    r'\b(where\s+is|directions\s+to|how\s+far)\b', re.I)),
            ],
            'file_io': [
                ('read_file', re.compile(
                    r'\b(read|open|load)\s+(the\s+)?(file|csv|json|txt|yaml|yml|xml)\b', re.I)),
                ('path', re.compile(
                    r'(\b[a-zA-Z]:\\[^:*?"<>|]+|\b/[^ \n]+|\b\.[/\\][^ \n]+)', re.I)),
                ('directory', re.compile(r'\b(directory|folder|path)\b', re.I)),
            ],
            'database': [
                ('sql_terms', re.compile(
                    r'\b(sql|database|table|row|column|schema|index|join)\b', re.I)),
                ('select_from', re.compile(r'\bselect\s+.+\s+from\s+.+', re.I)),
            ],
            'api_call': [
                ('http', re.compile(
                    r'\b(http\s*request|https?|endpoint|rest|graphql|api)\b', re.I)),
                ('curl', re.compile(
                    r'\b(curl\s+-[A-Za-z]+|GET|POST|PUT|DELETE)\b', re.I)),
            ],
            'rewrite': [
                ('rewrite', re.compile(
                    r'\b(rewrite|paraphrase|reword|polish|edit|improve\s+the\s+writing)\b', re.I)),
            ],
            'explain': [
                ('explain', re.compile(
                    r'\b(explain|why|how\s+does|walk\s+me\s+through|break\s+down)\b', re.I)),
            ],
            'compare': [
                ('compare', re.compile(r'\b(compare|vs\.?|difference\s+between)\b', re.I)),
            ],
            'outline': [
                ('outline', re.compile(
                    r'\b(outline|plan|steps|roadmap|bulleted\s+list)\b', re.I)),
            ],
        }

        self._context_map: Dict[str, List[str]] = {
            'web_search': ['web', 'network'],
            'code_gen': ['code'],
            'code_debug': ['code'],
            'summarize': ['document'],
            'translate': ['language_processing'],
            'sentiment': ['nlp'],
            'classify': ['nlp'],
            'math': ['calculator'],
            'date_time': ['current_time'],
            'location': ['geolocation'],
            'file_io': ['filesystem'],
            'database': ['database'],
            'api_call': ['network'],
            'rewrite': ['language_processing'],
            'explain': [],
            'compare': [],
            'outline': [],
        }

        self._tool_bias_map: Dict[str, List[str]] = {
            'web': ['web_search', 'api_call'],
            'browser': ['web_search'],
            'search': ['web_search'],
            'code': ['code_gen', 'code_debug'],
            'debug': ['code_debug'],
            'calculator': ['math'],
            'math': ['math'],
            'filesystem': ['file_io'],
            'file': ['file_io'],
            'sql': ['database'],
            'database': ['database'],
            'db': ['database'],
            'api': ['api_call'],
            'http': ['api_call'],
            'translate': ['translate'],
            'summarize': ['summarize'],
            'nlp': ['classify', 'sentiment', 'rewrite'],
        }

        self._language_keywords = [
            'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust', 'ruby', 'php',
            'kotlin', 'swift', 'r', 'matlab', 'sql', 'bash', 'shell', 'powershell'
        ]

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        """
        original = prompt or ''
        text = original.strip()
        lower = text.lower()

        detected: Dict[str, Dict[str, Any]] = {}
        for category, patterns in self._pattern_specs.items():
            count = 0
            examples: List[str] = []
            per_pattern_counts: Dict[str, int] = {}
            for label, regex in patterns:
                matches = list(regex.finditer(text))
                if matches:
                    per_pattern_counts[label] = len(matches)
                    count += len(matches)
                    for m in matches[:3]:
                        span = text[max(0, m.start() - 20)
                                        :min(len(text), m.end() + 20)]
                        examples.append(span.strip())
            if count > 0:
                base_conf = min(1.0, 0.2 * count)
                detected[category] = {
                    'count': count,
                    'by_pattern': per_pattern_counts,
                    'examples': examples[:5],
                    'confidence': base_conf,
                }

        entities = self._extract_entities(text)
        # Heuristic boosts based on entities
        if entities['urls']:
            self._boost_category(detected, 'web_search', 0.2)
            self._ensure_category_present(detected, 'web_search', [
                                          'url_present'], entities['urls'], base_conf=0.2)
        if entities['paths']:
            self._boost_category(detected, 'file_io', 0.2)
            self._ensure_category_present(
                detected, 'file_io', ['path'], entities['paths'], base_conf=0.2)
        if entities['code_blocks'] or entities['languages']:
            self._boost_category(detected, 'code_gen', 0.2)
        if any(k in lower for k in ['error', 'traceback', 'exception']) and (entities['code_blocks'] or 'code_gen' in detected):
            self._boost_category(detected, 'code_debug', 0.2)

        # Tool name bias
        tool_bias_labels = self._tool_bias_for(tool_name)
        for cat in tool_bias_labels:
            self._boost_category(detected, cat, 0.15)

        # Arguments-informed boosts
        arg_keys_lower = [str(k).lower() for k in (arguments or {}).keys()]
        if any(k in arg_keys_lower for k in ['url', 'urls', 'query']):
            self._boost_category(detected, 'web_search', 0.1)
        if any(k in arg_keys_lower for k in ['file', 'path', 'filepath', 'directory']):
            self._boost_category(detected, 'file_io', 0.1)
        if any(k in arg_keys_lower for k in ['sql', 'table', 'database', 'query']):
            self._boost_category(detected, 'database', 0.1)
        if any(k in arg_keys_lower for k in ['method', 'endpoint', 'headers', 'params', 'payload']):
            self._boost_category(detected, 'api_call', 0.1)
        if any(k in arg_keys_lower for k in ['text', 'content']) and re.search(r'\b(summarize|rewrite|translate)\b', lower):
            self._boost_category(detected, 'summarize', 0.1)
            self._boost_category(detected, 'rewrite', 0.05)
            self._boost_category(detected, 'translate', 0.05)

        # Normalize confidences
        for v in detected.values():
            v['confidence'] = max(
                0.0, min(1.0, round(float(v['confidence']), 3)))

        # Intents (sorted by confidence)
        intents = sorted(
            [{'label': k, 'confidence': v['confidence']}
                for k, v in detected.items()],
            key=lambda x: x['confidence'],
            reverse=True
        )

        # Required context inference
        required_context = set()
        for cat, info in detected.items():
            if info['confidence'] >= 0.4:
                for ctx in self._context_map.get(cat, []):
                    required_context.add(ctx)
        # Entity-driven contexts
        if entities['urls']:
            required_context.update(['web', 'network'])
        if entities['paths']:
            required_context.add('filesystem')
        if entities['dates']:
            required_context.add('current_time')
        if 'math' in detected and detected['math']['confidence'] >= 0.3:
            required_context.add('calculator')

        # Overall confidence
        overall_confidence = round(
            max([i['confidence'] for i in intents], default=0.0), 3)

        result: Dict[str, Any] = {
            'detected': detected,
            'entities': entities,
            'intents': intents,
            'required_context': sorted(required_context),
            'overall_confidence': overall_confidence,
        }
        return result

    def _tool_bias_for(self, tool_name: str) -> List[str]:
        if not tool_name:
            return []
        name = tool_name.lower()
        labels: List[str] = []
        for key, cats in self._tool_bias_map.items():
            if key in name:
                labels.extend(cats)
        return list(dict.fromkeys(labels))

    def _boost_category(self, detected: Dict[str, Dict[str, Any]], category: str, amount: float) -> None:
        if category in detected:
            detected[category]['confidence'] = min(
                1.0, detected[category]['confidence'] + amount)

    def _ensure_category_present(
        self,
        detected: Dict[str, Dict[str, Any]],
        category: str,
        labels: List[str],
        examples: List[str],
        base_conf: float = 0.15
    ) -> None:
        if category not in detected:
            detected[category] = {
                'count': 1,
                'by_pattern': {labels[0]: 1} if labels else {},
                'examples': examples[:3],
                'confidence': base_conf,
            }

    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        urls = re.findall(r'https?://[^\s)>\]"\'`]+', text, flags=re.I)
        emails = re.findall(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)
        numbers = re.findall(r'\b-?\d+(?:\.\d+)?\b', text)
        dates = []
        dates += re.findall(r'\b\d{4}-\d{2}-\d{2}\b', text)
        dates += re.findall(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', text)
        dates += re.findall(
            r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{1,2}(?:,\s*\d{4})?\b', text, flags=re.I)

        code_blocks = []
        for m in re.finditer(r'```(\w+)?\n?([\s\S]*?)```', text):
            code_blocks.append(m.group(0))

        # Inline code-like snippets
        inline_code = re.findall(r'`([^`]+)`', text)
        if inline_code:
            code_blocks.extend(['`' + s + '`' for s in inline_code])

        # File paths (Unix and Windows)
        paths = []
        # Windows
        paths += re.findall(r'\b[a-zA-Z]:\\(?:[^:*?"<>|\r\n]+\\?)+', text)
        # Unix-like
        paths += re.findall(r'(?:(?<=\s)|^)(?:/[^ \n]+|\.{1,2}/[^ \n]+)', text)

        languages = self._detect_languages(text)

        return {
            'urls': urls[:10],
            'emails': emails[:10],
            'numbers': numbers[:20],
            'dates': dates[:10],
            'code_blocks': code_blocks[:5],
            'paths': paths[:10],
            'languages': languages[:10],
        }

    def _detect_languages(self, text: str) -> List[str]:
        langs = set()
        # From code fences
        for m in re.finditer(r'```(\w+)?', text):
            lang = (m.group(1) or '').lower()
            if lang and lang in self._language_keywords:
                langs.add(lang)
        # From plain mentions
        for lang in self._language_keywords:
            if re.search(r'\b' + re.escape(lang) + r'\b', text, flags=re.I):
                langs.add(lang)
        return list(langs)
