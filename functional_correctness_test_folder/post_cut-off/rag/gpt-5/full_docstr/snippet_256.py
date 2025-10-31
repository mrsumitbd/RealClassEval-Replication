from typing import Any, Dict, List, Tuple, Optional, Pattern
import re
import string


class PromptPatternMatcher:
    """Analyzes prompts to determine context requirements."""

    def __init__(self):
        """Initialize pattern matchers."""
        # Core intent patterns with weights
        self.pattern_specs: List[Dict[str, Any]] = [
            {
                'name': 'definition',
                'regex': re.compile(r'^\s*(what|who)\s+is\b|^\s*define\b|^\s*explain\b', re.I),
                'weight': 0.3,
            },
            {
                'name': 'summarization',
                'regex': re.compile(r'\b(summarize|summary of|tl;dr|give me a summary)\b', re.I),
                'weight': 0.3,
            },
            {
                'name': 'comparison',
                'regex': re.compile(r'\b(compare|versus|vs\.?|difference between)\b', re.I),
                'weight': 0.25,
            },
            {
                'name': 'trend',
                'regex': re.compile(r'\b(trend|evolution|over time|time series|historical)\b', re.I),
                'weight': 0.35,
            },
            {
                'name': 'calculation',
                'regex': re.compile(r'\b(calculate|compute|sum|total|average|mean|median|std|standard deviation|correlation|regression)\b', re.I),
                'weight': 0.3,
            },
            {
                'name': 'aggregation',
                'regex': re.compile(r'\b(group by|aggregate|count by|bucket|bin)\b', re.I),
                'weight': 0.25,
            },
            {
                'name': 'time_range',
                'regex': re.compile(r'\b(last|this|next)\s+(year|month|week|quarter)\b|\b(yesterday|today|tomorrow)\b|\b(past|previous|last)\s+\d+\s+(days|weeks|months|years)\b|\bbetween\s+.+?\s+and\s+.+?\b|\bfrom\s+.+?\s+(to|-)\s+.+?\b|\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b(in|since|during)\s+(19|20)\d{2}\b', re.I),
                'weight': 0.25,
            },
            {
                'name': 'news_recency',
                'regex': re.compile(r'\b(latest|recent|breaking|news|today)\b', re.I),
                'weight': 0.3,
            },
            {
                'name': 'question',
                'regex': re.compile(r'\?\s*$', re.M),
                'weight': 0.05,
            },
            {
                'name': 'code_explanation',
                'regex': re.compile(r'\b(explain (this )?(code|function|snippet)|what does this code do)\b', re.I),
                'weight': 0.3,
            },
            {
                'name': 'code_generation',
                'regex': re.compile(r'\b(write|generate|implement|create)\b.*\b(code|function|class|script)\b', re.I),
                'weight': 0.35,
            },
            {
                'name': 'sql_query',
                'regex': re.compile(r'\bselect\b.+\bfrom\b|\b(join|where|group by|order by)\b', re.I | re.S),
                'weight': 0.4,
            },
            {
                'name': 'plotting',
                'regex': re.compile(r'\b(plot|chart|graph|visualize|visualise|visualization|visualisation)\b', re.I),
                'weight': 0.2,
            },
            {
                'name': 'translation',
                'regex': re.compile(r'\b(translate|traduce|übersetze|traduire)\b', re.I),
                'weight': 0.25,
            },
            {
                'name': 'sentiment',
                'regex': re.compile(r'\b(sentiment|positiv(e)?|negativ(e)?|neutral)\b', re.I),
                'weight': 0.2,
            },
        ]

        # Month names for simple date recognition
        months = [
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'sept', 'oct', 'nov', 'dec'
        ]
        self.months_set = set(months)
        self.month_pattern: Pattern[str] = re.compile(
            r'\b(' + '|'.join(months) +
            r')\b(?:\s+\d{1,2}(?:,\s*\d{2,4})?)?', re.I
        )
        # Year pattern
        self.year_pattern: Pattern[str] = re.compile(r'\b(19|20)\d{2}\b')

        # Relative time patterns
        self.relative_time_patterns: List[Tuple[Pattern[str], str]] = [
            (re.compile(r'\byesterday\b', re.I), 'yesterday'),
            (re.compile(r'\btoday\b', re.I), 'today'),
            (re.compile(r'\btomorrow\b', re.I), 'tomorrow'),
            (re.compile(r'\blast\s+week\b', re.I), 'last_week'),
            (re.compile(r'\bthis\s+week\b', re.I), 'this_week'),
            (re.compile(r'\bnext\s+week\b', re.I), 'next_week'),
            (re.compile(r'\blast\s+month\b', re.I), 'last_month'),
            (re.compile(r'\bthis\s+month\b', re.I), 'this_month'),
            (re.compile(r'\bnext\s+month\b', re.I), 'next_month'),
            (re.compile(r'\blast\s+year\b', re.I), 'last_year'),
            (re.compile(r'\bthis\s+year\b', re.I), 'this_year'),
            (re.compile(r'\bnext\s+year\b', re.I), 'next_year'),
            (re.compile(r'\b(past|previous|last)\s+(\d+)\s+(days|weeks|months|years)\b',
             re.I), 'rolling_window'),
        ]

        # Explicit date patterns (ISO and common)
        self.iso_date_pattern: Pattern[str] = re.compile(
            r'\b\d{4}-\d{2}-\d{2}\b')
        self.slash_date_pattern: Pattern[str] = re.compile(
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b')

        # Range patterns
        self.range_between_pattern: Pattern[str] = re.compile(
            r'\bbetween\s+(.+?)\s+and\s+(.+?)\b', re.I)
        self.range_from_to_pattern: Pattern[str] = re.compile(
            r'\bfrom\s+(.+?)\s+(?:to|-)\s+(.+?)\b', re.I)

        # Numeric and unit patterns
        self.currency_pattern: Pattern[str] = re.compile(
            r'(\$|€|£)\s?\d+(?:,\d{3})*(?:\.\d+)?|\bUSD\s?\d+|\bEUR\s?\d+|\bGBP\s?\d+', re.I)
        self.percent_pattern: Pattern[str] = re.compile(r'\b\d+(?:\.\d+)?\s?%')
        self.number_pattern: Pattern[str] = re.compile(r'\b\d+(?:\.\d+)?\b')

        # Ambiguity indicators
        self.ambiguity_pattern: Pattern[str] = re.compile(
            r'\b(this|that|it|they|above|previous|earlier|context)\b', re.I)

        # Language hints for translation target detection
        self.languages = {
            'english': 'en', 'spanish': 'es', 'french': 'fr', 'german': 'de', 'italian': 'it',
            'portuguese': 'pt', 'russian': 'ru', 'chinese': 'zh', 'japanese': 'ja', 'korean': 'ko',
            'hindi': 'hi', 'arabic': 'ar'
        }
        self.translate_to_pattern: Pattern[str] = re.compile(
            r'\btranslate\s+(?:this|the|it)?\s*(?:text|sentence|paragraph|document|content)?\s*(?:to|into)\s+([a-z]+)\b',
            re.I
        )

        # Domain keyword sets
        self.finance_keywords = re.compile(
            r'\b(stock|market|revenue|profit|sales|interest|inflation|gdp|crypto|bitcoin|ethereum|eth|btc|nasdaq|dow jones)\b', re.I)
        self.health_keywords = re.compile(
            r'\b(patient|disease|covid|symptom|treatment|diagnosis|drug|vaccine|epidemic|pandemic)\b', re.I)
        self.tech_keywords = re.compile(
            r'\b(server|database|api|python|java|sql|docker|kubernetes|microservice|endpoint)\b', re.I)

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        """
        text = prompt or ""
        lowered = text.lower()

        # Detect matched patterns
        matched_patterns: Dict[str, Dict[str, Any]] = {}
        total_weight = 0.0
        for spec in self.pattern_specs:
            matches = list(spec['regex'].finditer(text))
            if matches:
                spans = [(m.start(), m.end(), text[m.start():m.end()])
                         for m in matches]
                matched_patterns[spec['name']] = {
                    'matched': True,
                    'confidence': spec['weight'],
                    'spans': spans,
                }
                total_weight += spec['weight']

        # Extract entities
        entities: List[Dict[str, Any]] = []
        entities.extend(self._extract_time_entities(text))
        entities.extend(self._extract_numeric_entities(text))
        # Simple quoted string entities (potential exact phrases or titles)
        for m in re.finditer(r'"([^"]+)"', text):
            entities.append({
                'type': 'PHRASE',
                'text': m.group(1),
                'span': (m.start(1), m.end(1)),
                'normalized': m.group(1),
            })

        # Language detection (very lightweight)
        language = 'en'
        translation_target = None
        to_match = self.translate_to_pattern.search(text)
        if to_match:
            lang_word = to_match.group(1).lower()
            translation_target = self.languages.get(lang_word, lang_word)
            language = 'en'  # Source language assumed unknown; keep 'en' as interface language
            entities.append({
                'type': 'LANGUAGE',
                'text': lang_word,
                'span': (to_match.start(1), to_match.end(1)),
                'normalized': translation_target,
            })

        # Domains
        domains: List[str] = []
        if self.finance_keywords.search(text):
            domains.append('finance')
        if self.health_keywords.search(text):
            domains.append('health')
        if self.tech_keywords.search(text):
            domains.append('technology')

        # Requirements derivation
        needs_datetime_resolution = any(e['type'] == 'DATE' for e in entities)
        needs_historical_context = 'trend' in matched_patterns or (needs_datetime_resolution and any(
            self._entity_is_range_like(e) for e in entities if e['type'] == 'DATE'
        ))
        needs_calculation = 'calculation' in matched_patterns or 'aggregation' in matched_patterns or any(
            e['type'] in ('PERCENT', 'NUMBER', 'CURRENCY') for e in entities
        )
        needs_structured_query = 'sql_query' in matched_patterns or 'aggregation' in matched_patterns
        needs_code_execution = 'code_generation' in matched_patterns or 'code_explanation' in matched_patterns
        needs_retrieval = any(k in matched_patterns for k in (
            'definition', 'news_recency', 'summarization')) or 'latest' in lowered
        needs_disambiguation = bool(self.ambiguity_pattern.search(
            text)) and not text.strip().endswith('?')

        # Time window extraction
        time_window = self._derive_time_window(text)

        # Tool adjustments
        tool_notes: List[str] = []
        confidence_delta = 0.0
        tool_l = (tool_name or '').lower()
        if tool_l:
            if any(k in tool_l for k in ('search', 'web', 'crawler')):
                if needs_retrieval:
                    confidence_delta += 0.05
                    tool_notes.append('Tool aligned with retrieval needs.')
                else:
                    tool_notes.append(
                        'Retrieval-capable tool; prompt may not need it.')
            if any(k in tool_l for k in ('sql', 'database', 'db', 'warehouse')):
                if needs_structured_query:
                    confidence_delta += 0.05
                    tool_notes.append(
                        'Tool aligned with structured query needs.')
                else:
                    confidence_delta -= 0.02
                    tool_notes.append('SQL/database tool may be unnecessary.')
            if any(k in tool_l for k in ('code', 'python', 'runtime', 'execute', 'notebook')):
                if needs_code_execution or needs_calculation:
                    confidence_delta += 0.05
                    tool_notes.append(
                        'Tool aligned with code execution/calculation needs.')
                else:
                    confidence_delta -= 0.02
                    tool_notes.append('Execution tool may be unnecessary.')

        # Aggregate confidence
        base_conf = min(0.95, total_weight)
        # Slight boost for coherent combinations
        if 'trend' in matched_patterns and needs_datetime_resolution:
            base_conf = min(0.95, base_conf + 0.05)
        if 'comparison' in matched_patterns and any(w in lowered for w in ('and', 'vs', 'versus')):
            base_conf = min(0.95, base_conf + 0.03)
        if entities:
            base_conf = min(0.95, base_conf + 0.02)
        overall_confidence = max(
            0.05, min(1.0, 0.05 + base_conf + confidence_delta))

        requirements = {
            'needs_datetime_resolution': needs_datetime_resolution,
            'time_window': time_window,
            'needs_external_knowledge': needs_retrieval,
            'needs_historical_context': needs_historical_context,
            'needs_retrieval': needs_retrieval,
            'needs_structured_query': needs_structured_query,
            'needs_code_execution': needs_code_execution,
            'needs_calculation': needs_calculation,
            'needs_disambiguation': needs_disambiguation,
            'language': language,
            'translation_target': translation_target,
            'domain': domains,
        }

        result = {
            'patterns': matched_patterns,
            'entities': entities,
            'requirements': requirements,
            'confidence': round(overall_confidence, 3),
            'tool_adjustments': {
                'tool_name': tool_name,
                'arguments': arguments,
                'confidence_delta': round(confidence_delta, 3),
                'notes': tool_notes,
            },
        }
        return result

    def _entity_is_range_like(self, e: Dict[str, Any]) -> bool:
        text = e.get('text', '').lower()
        return bool(re.search(r'\bbetween\b|\bfrom\b|\bto\b|\band\b', text)) or e.get('normalized', '').startswith('RELATIVE:')

    def _extract_time_entities(self, text: str) -> List[Dict[str, Any]]:
        entities: List[Dict[str, Any]] = []

        # Relative time
        for pat, label in self.relative_time_patterns:
            for m in pat.finditer(text):
                normalized = None
                if label == 'rolling_window':
                    # e.g., last 30 days
                    qty = None
                    unit = None
                    try:
                        qty = int(m.group(2))
                        unit = m.group(3).lower()
                    except Exception:
                        pass
                    normalized = f'ROLLING:{qty}_{unit}' if qty and unit else 'RELATIVE:rolling_window'
                else:
                    normalized = f'RELATIVE:{label}'
                entities.append({
                    'type': 'DATE',
                    'text': m.group(0),
                    'span': (m.start(), m.end()),
                    'normalized': normalized,
                })

        # Explicit ISO dates
        for m in self.iso_date_pattern.finditer(text):
            entities.append({
                'type': 'DATE',
                'text': m.group(0),
                'span': (m.start(), m.end()),
                'normalized': m.group(0),
            })

        # Slash dates
        for m in self.slash_date_pattern.finditer(text):
            entities.append({
                'type': 'DATE',
                'text': m.group(0),
                'span': (m.start(), m.end()),
                'normalized': m.group(0),
            })

        # Month + optional day/year
        for m in self.month_pattern.finditer(text):
            entities.append({
                'type': 'DATE',
                'text': m.group(0),
                'span': (m.start(), m.end()),
                'normalized': m.group(0),
            })

        # Years
        for m in self.year_pattern.finditer(text):
            entities.append({
                'type': 'DATE',
                'text': m.group(0),
                'span': (m.start(), m.end()),
                'normalized': m.group(0),
            })

        # Ranges
        for m in self.range_between_pattern.finditer(text):
            entities.append({
                'type': 'DATE',
                'text': m.group(0),
                'span': (m.start(), m.end()),
                'normalized': f'RANGE:{m.group(1).strip()}→{m.group(2).strip()}',
            })
        for m in self.range_from_to_pattern.finditer(text):
            entities.append({
                'type': 'DATE',
                'text': m.group(0),
                'span': (m.start(), m.end()),
                'normalized': f'RANGE:{m.group(1).strip()}→{m.group(2).strip()}',
            })

        # Deduplicate by span and text
        dedup_key = set()
        deduped: List[Dict[str, Any]] = []
        for e in entities:
            key = (e['span'], e['text'])
            if key not in dedup_key:
                dedup_key.add(key)
                deduped.append(e)
        return deduped

    def _extract_numeric_entities(self, text: str) -> List[Dict[str, Any]]:
        entities: List[Dict[str, Any]] = []

        for m in self.currency_pattern.finditer(text):
            entities.append({
                'type': 'CURRENCY',
                'text': m.group(0),
                'span': (m.start(), m.end()),
                'normalized': m.group(0).replace(',', ''),
            })

        for m in self.percent_pattern.finditer(text):
            entities.append({
                'type': 'PERCENT',
                'text': m.group(0),
                'span': (m.start(), m.end()),
                'normalized': m.group(0).replace(' ', ''),
            })

        # Bare numbers (exclude those already covered by currency/percent using spans)
        covered_spans = []
        for e in entities:
            covered_spans.append(e['span'])
        for m in self.number_pattern.finditer(text):
            span = (m.start(), m.end())
            if any(span[0] >= s[0] and span[1] <= s[1] for s in covered_spans):
                continue
            entities.append({
                'type': 'NUMBER',
                'text': m.group(0),
                'span': span,
                'normalized': m.group(0),
            })

        return entities

    def _derive_time_window(self, text: str) -> Dict[str, Optional[str]]:
        # Try to find explicit ranges
        start = None
        end = None
        relative = None

        # Relative single expressions
        rels = []
        for pat, label in self.relative_time_patterns:
            for m in pat.finditer(text):
                if label == 'rolling_window':
                    try:
                        qty = int(m.group(2))
                        unit = m.group(3).lower()
                        rels.append(f'ROLLING:{qty}_{unit}')
                    except Exception:
                        rels.append('RELATIVE:rolling_window')
                else:
                    rels.append(f'RELATIVE:{label}')
        if rels:
            # Prefer the first detected relative expression
            relative = rels[0]

        # Range via 'between'
        m = self.range_between_pattern.search(text)
        if m:
            start = m.group(1).strip(string.punctuation + ' ')
            end = m.group(2).strip(string.punctuation + ' ')
            relative = None

        # Range via 'from ... to ...'
        m = self.range_from_to_pattern.search(text)
        if m:
            start = m.group(1).strip(string.punctuation + ' ')
            end = m.group(2).strip(string.punctuation + ' ')
            relative = None

        # If explicit ISO dates appear twice, treat as a range in order of appearance
        iso_dates = [mm.group(0)
                     for mm in self.iso_date_pattern.finditer(text)]
        if len(iso_dates) >= 2 and not (start and end):
            start, end = iso_dates[0], iso_dates[1]
            relative = None

        return {'start': start, 'end': end, 'relative': relative}
