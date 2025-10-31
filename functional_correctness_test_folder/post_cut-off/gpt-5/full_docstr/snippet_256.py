from typing import Dict, Any, List, Tuple
import re


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        # Core intent keywords
        self.intent_keywords = {
            "summarize": [r"\bsummariz(e|e it|ation)\b", r"\btl;?dr\b"],
            "compare": [r"\bcompare\b", r"\bdifference(s)? between\b", r"\bvs\.?\b"],
            "troubleshoot": [r"\b(troubleshoot|debug|fix|why.*not working|error)\b"],
            "generate": [r"\bgenerate\b", r"\bcreate\b", r"\bwrite\b", r"\bproduce\b", r"\bbuild\b"],
            "explain": [r"\bexplain\b", r"\bwhat is\b", r"\bhow does\b", r"\bwhy is\b"],
            "translate": [r"\btranslate\b", r"\b(in|to) (english|spanish|french|german|chinese|japanese|korean)\b"],
            "extract": [r"\bextract\b", r"\bpull out\b", r"\bfind all\b"],
            "categorize": [r"\bcategorize\b", r"\bclassify\b", r"\bgroup\b", r"\blabel\b"],
            "sentiment": [r"\bsentiment\b", r"\bpositive or negative\b", r"\bopinion\b"],
            "calculate": [r"\bcalculate\b", r"\bcompute\b", r"\bestimate\b"],
            "summon_data": [r"\blookup\b", r"\bfetch\b", r"\bget latest\b", r"\bcurrent\b", r"\bup[- ]to[- ]date\b"],
            "plan": [r"\bplan\b", r"\bitinerary\b", r"\bschedule\b", r"\broadmap\b"],
            "code": [r"\bcode\b", r"\bscript\b", r"\bfunction\b", r"\bclass\b", r"\bregex\b"],
        }

        # Entity patterns
        self.entity_patterns = {
            "dates": re.compile(r"\b(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{2,4}|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{1,2}(?:,\s*\d{4})?)\b", re.IGNORECASE),
            "times": re.compile(r"\b(?:\d{1,2}:\d{2}\s*(?:am|pm)?|\d{1,2}\s*(?:am|pm))\b", re.IGNORECASE),
            "locations": re.compile(r"\b(?:in|at|near|from)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\b"),
            # Simple proper names
            "people": re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b"),
            "organizations": re.compile(r"\b[A-Z][A-Za-z0-9&\-. ]+(?:Inc\.|Corp\.|LLC|Ltd\.|University|Institute|Committee|Foundation)\b"),
            "emails": re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+\b"),
            "urls": re.compile(r"\bhttps?://[^\s)>\]]+\b"),
            "versions": re.compile(r"\bv?(?:\d+\.)+\d+\b"),
            "numbers": re.compile(r"\b\d+(?:\.\d+)?\b"),
            "ips": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
            "files": re.compile(r"\b[\w,\s-]+\.(?:pdf|docx?|pptx?|xlsx?|csv|json|yaml|yml|xml|md|txt|py|js|ts|java|c|cpp|go|rb|php|ipynb)\b", re.IGNORECASE),
            "code_blocks": re.compile(r"```[\s\S]*?```|`[^`]+`"),
            "errors": re.compile(r"\b(?:Exception|Error|Traceback|stack trace|segmentation fault|timeout|500|404|NullPointerException|TypeError|ValueError)\b", re.IGNORECASE),
        }

        # Pattern detectors
        self.patterns = {
            "temporal": re.compile(r"\b(today|yesterday|tomorrow|last week|next week|last month|next month|this quarter|Q[1-4]\b|deadline|by\s+\w+day|since|until|between)\b", re.IGNORECASE),
            "spatial": re.compile(r"\b(in|at|near|from|to)\b.*\b(city|state|country|region|office|hq|headquarters|remote|onsite)\b", re.IGNORECASE),
            "comparative": re.compile(r"\b(vs\.?|versus|compare|better than|worse than|greater than|less than|higher than|lower than|compare to)\b", re.IGNORECASE),
            "statistical": re.compile(r"\b(mean|median|mode|std(?:\.| dev)?|variance|correlation|regression|p-?value|confidence interval)\b", re.IGNORECASE),
            "question": re.compile(r"^\s*(who|what|when|where|why|how|which|whom)\b", re.IGNORECASE),
            "instructional": re.compile(r"\b(step|steps|instruction|guide|how to|walkthrough|tutorial)\b", re.IGNORECASE),
            "file_request": re.compile(r"\b(upload|attach|open|read|parse)\b.*\b(file|document|dataset|csv|json|spreadsheet)\b", re.IGNORECASE),
            "data_freshness": re.compile(r"\b(current|latest|real[- ]time|up[- ]to[- ]date|as of|today)\b", re.IGNORECASE),
            "disambiguation": re.compile(r"\b(ambiguous|clarify|which one|do you mean|unclear|more details)\b", re.IGNORECASE),
            "privacy_sensitive": re.compile(r"\b(ssn|social security|credit card|password|api key|token|secret)\b", re.IGNORECASE),
        }

        # Tool affinities: simple hints per tool name
        self.tool_hints = {
            "web_search": ["current", "latest", "news", "trending", "today", "as of", "up to date", "source"],
            "code_runner": ["run", "execute", "script", "function", "error", "traceback", "compile", "test"],
            "file_reader": ["file", "document", "pdf", "csv", "xlsx", "attach", "upload", "parse", "open"],
            "database": ["query", "sql", "database", "table", "schema", "join", "aggregate"],
            "math": ["calculate", "compute", "sum", "integral", "derivative", "probability", "mean"],
        }

    def _collect_entities(self, prompt: str) -> Dict[str, Any]:
        entities: Dict[str, Any] = {}
        for name, pattern in self.entity_patterns.items():
            matches = list(pattern.finditer(prompt))
            values = [m.group(0) if name != "locations" else m.group(1)
                      for m in matches]
            entities[name] = {
                "values": values,
                "count": len(values)
            }
        return entities

    def _detect_intents(self, prompt: str) -> List[Dict[str, Any]]:
        intents: List[Dict[str, Any]] = []
        lower = prompt.lower()
        for label, kws in self.intent_keywords.items():
            hits = 0
            for kw in kws:
                if re.search(kw, lower):
                    hits += 1
            if hits:
                # Confidence scales with number of keyword matches
                conf = min(1.0, 0.4 + 0.2 * hits)
                intents.append({"label": label, "confidence": round(conf, 3)})
        # If no explicit intent, infer question vs request
        if not intents:
            if re.search(self.patterns["question"], prompt):
                intents.append({"label": "explain", "confidence": 0.5})
            elif re.search(r"[.!?]\s*$", prompt) is None or re.search(r"\bplease\b", lower):
                intents.append({"label": "generate", "confidence": 0.4})
        return intents

    def _detect_patterns(self, prompt: str) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        for name, pattern in self.patterns.items():
            hits = len(list(pattern.finditer(prompt)))
            results[name] = {"matched": bool(hits), "count": hits}
        # Additional derived patterns
        results["contains_numbers"] = {"matched": bool(re.search(self.entity_patterns["numbers"], prompt)), "count": len(
            list(self.entity_patterns["numbers"].finditer(prompt)))}
        results["is_question"] = {"matched": bool(re.search(r"\?\s*$", prompt) or re.search(self.patterns["question"], prompt)), "count": 1 if (
            re.search(r"\?\s*$", prompt) or re.search(self.patterns["question"], prompt)) else 0}
        return results

    def _infer_context_requirements(self, entities: Dict[str, Any], patterns: Dict[str, Any], intents: List[Dict[str, Any]], tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        needs_timeframe = patterns.get("temporal", {}).get(
            "matched") or entities.get("dates", {}).get("count", 0) > 0
        needs_location = patterns.get("spatial", {}).get(
            "matched") or entities.get("locations", {}).get("count", 0) > 0
        needs_data_freshness = patterns.get("data_freshness", {}).get(
            "matched") or any(i["label"] == "summon_data" for i in intents)
        needs_files = patterns.get("file_request", {}).get(
            "matched") or entities.get("files", {}).get("count", 0) > 0
        needs_code_execution = any(i["label"] in ("code", "troubleshoot") for i in intents) or entities.get(
            "code_blocks", {}).get("count", 0) > 0 or entities.get("errors", {}).get("count", 0) > 0
        needs_disambiguation = patterns.get("disambiguation", {}).get("matched") or (entities.get(
            "people", {}).get("count", 0) + entities.get("organizations", {}).get("count", 0) > 3)
        privacy_sensitive = patterns.get(
            "privacy_sensitive", {}).get("matched")

        # Arguments can fulfill certain requirements
        if arguments:
            if any(k in arguments for k in ("date", "start_date", "end_date", "timeframe")):
                needs_timeframe = False
            if any(k in arguments for k in ("location", "region", "city", "country")):
                needs_location = False
            if any(k in arguments for k in ("file", "files", "path", "paths", "blob")):
                needs_files = False

        # Tool name influences browsing/data freshness
        tool_lower = (tool_name or "").lower()
        if "web" in tool_lower or "search" in tool_lower or "browser" in tool_lower:
            # The tool supports freshness
            needs_data_freshness = False

        return {
            "needs_timeframe": bool(needs_timeframe),
            "needs_location": bool(needs_location),
            "needs_data_freshness": bool(needs_data_freshness),
            "needs_files": bool(needs_files),
            "needs_code_execution": bool(needs_code_execution),
            "needs_disambiguation": bool(needs_disambiguation),
            "contains_sensitive": bool(privacy_sensitive),
        }

    def _tool_alignment(self, prompt: str, tool_name: str) -> Dict[str, Any]:
        tool = (tool_name or "").lower()
        if not tool:
            return {"tool_name": tool_name, "fit_score": 0.5, "notes": "No tool specified"}
        hints = self.tool_hints.get(tool, [])
        if not hints:
            # Try partial match keys
            for k, v in self.tool_hints.items():
                if k in tool:
                    hints = v
                    break
        score = 0.5
        notes = []
        if hints:
            matches = sum(1 for h in hints if re.search(
                rf"\b{re.escape(h)}\b", prompt.lower()))
            score = min(1.0, 0.4 + 0.15 * matches)
            if matches:
                notes.append(f"Matched {matches} hint(s)")
        else:
            notes.append("No hints for tool")
        return {"tool_name": tool_name, "fit_score": round(score, 3), "notes": "; ".join(notes) or "n/a"}

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        if not isinstance(prompt, str) or not prompt.strip():
            return {
                "intents": [],
                "entities": {},
                "patterns": {},
                "context_requirements": {},
                "tool_alignment": {"tool_name": tool_name, "fit_score": 0.0, "notes": "Empty prompt"},
                "confidence": 0.0,
            }

        prompt = prompt.strip()
        entities = self._collect_entities(prompt)
        patterns = self._detect_patterns(prompt)
        intents = self._detect_intents(prompt)

        context_requirements = self._infer_context_requirements(
            entities, patterns, intents, tool_name, arguments or {})
        tool_alignment = self._tool_alignment(prompt, tool_name)

        # Overall confidence heuristic
        signal_counts = [
            sum(1 for i in intents if i["confidence"] >= 0.6),
            sum(v["count"] for v in entities.values()),
            sum(1 for p in patterns.values() if p.get("matched")),
        ]
        raw = 0.2 + 0.15 * min(6, len(intents)) + 0.1 * min(10,
                                                            signal_counts[1]) + 0.1 * min(6, signal_counts[2])
        confidence = round(min(1.0, raw), 3)

        return {
            "intents": intents,
            "entities": entities,
            "patterns": patterns,
            "context_requirements": context_requirements,
            "tool_alignment": tool_alignment,
            "confidence": confidence,
        }
