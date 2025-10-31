from typing import Dict, Any, List, Pattern, Tuple, Optional
import re


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        self.patterns: Dict[str, List[Tuple[str, Pattern]]] = {
            "web": [
                ("ask_search", re.compile(
                    r"\b(search|google|bing|duckduckgo|look up|find info|latest|current)\b", re.I)),
                ("ask_website", re.compile(
                    r"\b(on|from)\s+the\s+web\b|\bonline\b|\bwebsite\b", re.I)),
                ("url_present", re.compile(r"https?://", re.I)),
                ("news", re.compile(r"\bnews|today|recent|update|trending\b", re.I)),
            ],
            "file": [
                ("file_path", re.compile(
                    r"(?:[A-Za-z]:\\|/home/|/usr/|/var/|/etc/|~\/|\.txt\b|\.csv\b|\.json\b|\.pdf\b|\.md\b|\.docx?\b)", re.I)),
                ("file_ops", re.compile(
                    r"\b(read|write|open|load|save|parse)\b.*\b(file|document|dataset)\b", re.I)),
            ],
            "database": [
                ("sql_terms", re.compile(
                    r"\b(SQL|select|insert|update|delete|join|table|schema|database)\b", re.I)),
                ("db_ops", re.compile(r"\b(query|run|execute)\b.*\b(query|sql)\b", re.I)),
            ],
            "code": [
                ("lang_python", re.compile(
                    r"\bpython|pip|venv|numpy|pandas|pytest\b", re.I)),
                ("code_request", re.compile(
                    r"\b(write|implement|fix|debug|refactor|optimize)\b.*\b(code|function|class|script)\b", re.I)),
                ("snippet_marker", re.compile(
                    r"```|def\s+\w+\(|class\s+\w+", re.I)),
            ],
            "math": [
                ("equation", re.compile(
                    r"[\d\.\)\(]+[\+\-\*\/\^][\d\.\)\(]+")),
                ("math_words", re.compile(
                    r"\bcompute|calculate|derivative|integral|probability|sum|mean|median|variance|std\b", re.I)),
            ],
            "image": [
                ("image_ops", re.compile(
                    r"\bimage|picture|photo|png|jpg|jpeg|svg|plot|chart|diagram|visualize\b", re.I)),
                ("image_gen", re.compile(
                    r"\b(generate|create|draw|render)\b.*\b(image|picture|logo|icon|diagram)\b", re.I)),
            ],
            "audio": [
                ("audio_terms", re.compile(
                    r"\baudio|sound|mp3|wav|transcribe|speech|voice\b", re.I)),
            ],
            "video": [
                ("video_terms", re.compile(
                    r"\bvideo|mp4|youtube|frame rate|subtitle|caption\b", re.I)),
            ],
            "schedule": [
                ("calendar", re.compile(
                    r"\b(schedule|calendar|meeting|appointment|remind|reminder)\b", re.I)),
                ("time_phrases", re.compile(
                    r"\b(tomorrow|next week|today at|on \w+day at)\b", re.I)),
            ],
            "email": [
                ("email_ops", re.compile(
                    r"\bemail|inbox|send mail|draft|subject|recipient\b", re.I)),
            ],
            "summary": [
                ("summarize", re.compile(
                    r"\bsummar(y|ise|ize)|tl;dr|brief|condense|overview\b", re.I)),
            ],
            "translation": [
                ("translate", re.compile(
                    r"\btranslate|translation|into\b.*\b(english|spanish|french|german|chinese|japanese)\b", re.I)),
            ],
            "sentiment": [
                ("sentiment", re.compile(
                    r"\bsentiment|positive|negative|neutral|tone analysis\b", re.I)),
            ],
            "extraction": [
                ("extract", re.compile(
                    r"\bextract|pull out|parse\b.*\b(emails|names|dates|addresses|urls|entities)\b", re.I)),
            ],
            "reasoning": [
                ("chain_of_thought", re.compile(
                    r"\bstep by step|show (your )?work|reason (it )?out\b", re.I)),
                ("logic", re.compile(r"\bif.*then|therefore|because\b", re.I)),
            ],
            "creative": [
                ("creative", re.compile(
                    r"\bstory|poem|poetry|lyrics|creative|brainstorm|ideas\b", re.I)),
            ],
            "security": [
                ("security", re.compile(
                    r"\bpassword|token|api key|auth|jwt|oauth|hash|encrypt|decrypt\b", re.I)),
            ],
            "pii": [
                ("pii", re.compile(
                    r"\bssn|social security|credit card|cvv|dob|date of birth|phone number|email address\b", re.I)),
            ],
            "geolocation": [
                ("geo", re.compile(
                    r"\bcoordinates|latitude|longitude|gps|geocode|address\b", re.I)),
            ],
            "time_sensitive": [
                ("time", re.compile(
                    r"\bnow|currently|as of|real[- ]?time|today\b", re.I)),
            ],
        }

        self.category_requirements: Dict[str, List[str]] = {
            "web": ["internet"],
            "file": ["filesystem"],
            "database": ["database"],
            "code": ["python_runtime"],
            "math": ["calculator"],
            "image": ["image_tools"],
            "audio": ["audio_tools"],
            "video": ["video_tools"],
            "schedule": ["calendar_access"],
            "email": ["email_access"],
            "summary": ["text_processing"],
            "translation": ["text_processing"],
            "sentiment": ["text_processing"],
            "extraction": ["text_processing"],
            "reasoning": ["no_external_tools"],
            "creative": ["no_external_tools"],
            "security": ["safety_review"],
            "pii": ["safety_review"],
            "geolocation": ["maps"],
            "time_sensitive": ["internet"],
        }

        self.intent_priority: List[str] = [
            "web",
            "file",
            "database",
            "code",
            "math",
            "summary",
            "translation",
            "extraction",
            "sentiment",
            "image",
            "audio",
            "video",
            "schedule",
            "email",
            "geolocation",
            "security",
            "pii",
            "creative",
            "reasoning",
            "time_sensitive",
        ]

        self.tool_hints: Dict[str, List[str]] = {
            "internet": ["browser", "web", "search", "bing", "google", "duckduckgo", "serp", "news"],
            "filesystem": ["file", "fs", "drive", "storage", "readfile", "writefile"],
            "database": ["db", "database", "sql", "postgres", "mysql", "sqlite", "mongo"],
            "python_runtime": ["python", "execute", "code", "jupyter", "notebook", "runtime"],
            "calculator": ["calc", "math", "wolfram", "compute", "calculator"],
            "image_tools": ["image", "plot", "chart", "viz", "matplotlib", "graph"],
            "audio_tools": ["audio", "voice", "speech", "transcribe", "whisper"],
            "video_tools": ["video", "frames", "subtitle", "caption"],
            "calendar_access": ["calendar", "schedule", "meeting", "remind"],
            "email_access": ["email", "gmail", "inbox", "send"],
            "text_processing": ["summar", "translate", "extract", "sentiment", "nlp"],
            "maps": ["map", "geo", "location", "coordinates"],
            "safety_review": ["safety", "moderation", "redact"],
            "no_external_tools": ["reason", "think", "explain"],
        }

        self.url_re = re.compile(r"https?://[^\s]+", re.I)
        self.email_re = re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
        self.filepath_re = re.compile(
            r"(?:[A-Za-z]:\\[^\s]+|/[^ \n\t]+|~\/[^ \n\t]+)")
        self.date_re = re.compile(
            r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4}|\w+\s\d{1,2},\s?\d{4})\b")
        self.number_re = re.compile(r"\b\d+(?:\.\d+)?\b")

    def _normalize(self, s: str) -> str:
        return (s or "").strip()

    def _match_categories(self, prompt: str) -> Dict[str, List[str]]:
        matched: Dict[str, List[str]] = {}
        for category, rules in self.patterns.items():
            hits: List[str] = []
            for name, regex in rules:
                if regex.search(prompt):
                    hits.append(name)
            if hits:
                matched[category] = hits
        return matched

    def _infer_intent(self, matched: Dict[str, List[str]]) -> str:
        if not matched:
            return "general"
        for category in self.intent_priority:
            if category in matched:
                mapping = {
                    "web": "web_research",
                    "file": "file_io",
                    "database": "database_query",
                    "code": "coding",
                    "math": "math_computation",
                    "summary": "summarization",
                    "translation": "translation",
                    "sentiment": "sentiment_analysis",
                    "extraction": "information_extraction",
                    "image": "image_processing",
                    "audio": "audio_processing",
                    "video": "video_processing",
                    "schedule": "scheduling",
                    "email": "email_management",
                    "geolocation": "geolocation",
                    "security": "security",
                    "pii": "pii_handling",
                    "creative": "creative_writing",
                    "reasoning": "reasoning",
                    "time_sensitive": "time_sensitive",
                }
                return mapping.get(category, category)
        return "general"

    def _requirements_from_matches(self, matched: Dict[str, List[str]]) -> List[str]:
        reqs: List[str] = []
        for category in matched:
            reqs.extend(self.category_requirements.get(category, []))
        # unique while preserving order
        seen = set()
        uniq = []
        for r in reqs:
            if r not in seen:
                seen.add(r)
                uniq.append(r)
        return uniq

    def _tool_alignment(self, tool_name: str, requirements: List[str], arguments: Dict[str, Any]) -> Dict[str, Any]:
        tn = (tool_name or "").lower()
        reasons: List[str] = []
        matches = 0
        for req in requirements:
            hints = self.tool_hints.get(req, [])
            if any(h in tn for h in hints):
                matches += 1
                reasons.append(f"{req} hinted by tool name")
        # Infer from arguments
        arg_text = " ".join([str(v)
                            for v in (arguments or {}).values()]).lower()
        for req in requirements:
            hints = self.tool_hints.get(req, [])
            if any(h in arg_text for h in hints):
                matches += 1
                reasons.append(f"{req} hinted by arguments")
        # if no requirements, any tool is acceptable
        matched = matches > 0 or not requirements
        reason = "; ".join(reasons) if reasons else (
            "no specific requirements" if not requirements else "no clear alignment")
        return {"matches_tool": matched, "reason": reason}

    def _extract_entities(self, prompt: str) -> Dict[str, List[str]]:
        urls = self.url_re.findall(prompt)
        emails = self.email_re.findall(prompt)
        filepaths = self.filepath_re.findall(prompt)
        dates = self.date_re.findall(prompt)
        numbers = self.number_re.findall(prompt)
        return {
            "urls": urls,
            "emails": emails,
            "filepaths": filepaths,
            "dates": dates,
            "numbers": numbers,
        }

    def _confidence(self, matched: Dict[str, List[str]], entities: Dict[str, List[str]]) -> float:
        base = 0.3 if matched else 0.15
        strength = sum(len(v) for v in matched.values())
        conf = base + 0.1 * min(strength, 5)
        if any(entities.get(k) for k in ("urls", "filepaths", "dates")):
            conf += 0.05
        return max(0.0, min(conf, 0.98))

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        text = self._normalize(prompt)
        if not text:
            return {
                "intent": "general",
                "requires": [],
                "confidence": 0.1,
                "matched_patterns": {},
                "tool_alignment": {"matches_tool": True, "reason": "empty prompt"},
                "entities": {"urls": [], "emails": [], "filepaths": [], "dates": [], "numbers": []},
            }

        matched = self._match_categories(text)
        intent = self._infer_intent(matched)
        requirements = self._requirements_from_matches(matched)
        entities = self._extract_entities(text)

        # Heuristic: if time-sensitive phrasing and no explicit web, add internet
        if "time_sensitive" in matched and "internet" not in requirements:
            requirements.append("internet")

        # Heuristic: if code intent but math present, still python_runtime is enough
        # Heuristic: if summary intent and a URL detected, ensure internet
        if intent == "summarization" and entities.get("urls") and "internet" not in requirements:
            requirements.append("internet")

        alignment = self._tool_alignment(
            tool_name, requirements, arguments or {})
        confidence = self._confidence(matched, entities)

        return {
            "intent": intent,
            "requires": requirements,
            "confidence": confidence,
            "matched_patterns": matched,
            "tool_alignment": alignment,
            "entities": entities,
        }
