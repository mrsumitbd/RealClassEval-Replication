from typing import Tuple, Dict, List
import re
from collections import Counter


class DocumentAnalyzer:
    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        if not content or not content.strip():
            return ("unknown", 0.0)

        content_lower = content.lower()

        doc_profiles: Dict[str, Dict[str, object]] = {
            "research_paper": {
                "indicators": {
                    "strong": [
                        "abstract", "introduction", "methods", "methodology", "results",
                        "discussion", "conclusion", "references", "literature review",
                        "related work", "experiment", "dataset", "evaluation", "hypothesis"
                    ],
                    "medium": [
                        "we propose", "we present", "in this paper", "our contributions",
                        "statistical significance", "confidence interval", "p-value",
                        "baseline", "state-of-the-art", "novel", "theorem", "lemma"
                    ],
                    "weak": [
                        "appendix", "figure", "table", "citation", "study", "analysis",
                        "framework", "model", "approach"
                    ],
                },
                "patterns": [
                    r"abstract\s*\n", r"introduction\s*\n", r"conclusion[s]?\s*\n",
                    r"references\s*\n", r"\[\d+\]", r"\(fig\.?\s*\d+\)", r"doi:\s*\S+",
                ],
            },
            "technical_spec": {
                "indicators": {
                    "strong": [
                        "requirements", "specification", "scope", "non-functional",
                        "functional requirements", "acceptance criteria", "constraints",
                        "assumptions", "dependencies", "compliance", "standards"
                    ],
                    "medium": [
                        "shall", "must", "should", "will", "system shall", "component",
                        "interface", "protocol", "versioning", "backward compatibility"
                    ],
                    "weak": [
                        "diagram", "module", "architecture", "configuration",
                        "performance", "latency", "throughput"
                    ],
                },
                "patterns": [
                    r"\bshall\b", r"\brequirements\b", r"\bacceptance criteria\b",
                    r"\bnon[- ]functional\b", r"\bscope\b"
                ],
            },
            "tutorial": {
                "indicators": {
                    "strong": [
                        "step-by-step", "step 1", "step 2", "tutorial", "guide",
                        "walkthrough", "let's build", "in this tutorial", "how to"
                    ],
                    "medium": [
                        "prerequisites", "follow along", "you will learn", "next we",
                        "first, ", "then, ", "finally, "
                    ],
                    "weak": [
                        "tip", "note", "warning", "example", "demo", "hands-on",
                        "exercise"
                    ],
                },
                "patterns": [
                    r"^\s*\d+\.\s", r"^step\s*\d+", r"```", r"\bprerequisites\b",
                    r"\bhow to\b", r"\bin this tutorial\b"
                ],
            },
            "api_reference": {
                "indicators": {
                    "strong": [
                        "endpoint", "parameters", "returns", "response", "request",
                        "status codes", "authentication", "authorization",
                        "deprecation", "query parameter", "path parameter"
                    ],
                    "medium": [
                        "method signature", "arguments", "type", "default", "example",
                        "curl", "json", "yaml", "schema"
                    ],
                    "weak": [
                        "rate limit", "retry", "pagination", "oauth", "token",
                        "header", "body"
                    ],
                },
                "patterns": [
                    r"GET\s+/[^\s]+", r"POST\s+/[^\s]+", r"PUT\s+/[^\s]+", r"DELETE\s+/[^\s]+",
                    r"^Parameters", r"^Returns", r"```(json|yaml|http|bash)?",
                    r"\bHTTP/1\.[01]\b", r"\b200\b|\b404\b|\b401\b|\b500\b"
                ],
            },
            "design_doc": {
                "indicators": {
                    "strong": [
                        "design", "architecture", "trade-offs", "alternatives",
                        "non-goals", "goals", "constraints", "risks", "mitigation",
                        "scalability", "reliability", "availability", "consistency"
                    ],
                    "medium": [
                        "component", "module", "interface", "api", "sequence diagram",
                        "data flow", "er diagram", "cons", "pros"
                    ],
                    "weak": [
                        "monitoring", "observability", "alerting", "deployment",
                        "rollout", "migration"
                    ],
                },
                "patterns": [
                    r"\btrade[- ]offs?\b", r"\bnon[- ]goals?\b", r"\brisk[s]?\b",
                    r"\bmitigation[s]?\b", r"\balternative[s]?\b"
                ],
            },
            "report": {
                "indicators": {
                    "strong": [
                        "executive summary", "findings", "recommendations", "scope",
                        "methodology", "conclusion", "summary"
                    ],
                    "medium": [
                        "analysis", "overview", "observation", "data", "chart", "table"
                    ],
                    "weak": [
                        "appendix", "figure", "graph", "timeline", "outlook"
                    ],
                },
                "patterns": [
                    r"\bexecutive summary\b", r"\bfindings\b", r"\brecommendations\b",
                    r"\bmethodology\b"
                ],
            },
            "blog_post": {
                "indicators": {
                    "strong": [
                        "introduction", "conclusion", "thoughts", "opinion", "insights",
                        "story", "journey"
                    ],
                    "medium": [
                        "i think", "in my experience", "we found", "lessons learned",
                        "takeaways"
                    ],
                    "weak": [
                        "subscribe", "follow", "comment", "share", "like"
                    ],
                },
                "patterns": [
                    r"^#\s", r"^##\s", r"\bsubscribe\b", r"\bcomment\b", r"\bshare\b"
                ],
            },
        }

        scores: Dict[str, float] = {}
        impl_detail = self._calculate_implementation_detail_level(
            content_lower)
        concept_complex = self._calculate_concept_complexity(content_lower)

        for doc_type, profile in doc_profiles.items():
            indicators = profile["indicators"]  # type: ignore
            patterns = profile["patterns"]      # type: ignore

            weighted = self._calculate_weighted_score(
                content_lower, indicators)  # type: ignore
            pscore = self._detect_pattern_score(
                content_lower, patterns)          # type: ignore

            base = 0.65 * weighted + 0.35 * pscore

            if doc_type == "tutorial":
                base += 0.10 * impl_detail
            elif doc_type == "research_paper":
                base += 0.10 * concept_complex + \
                    0.05 * max(0.0, 1.0 - impl_detail)
            elif doc_type == "api_reference":
                base += 0.15 * impl_detail
            elif doc_type == "technical_spec":
                base += 0.10 * (0.5 * concept_complex + 0.5 * impl_detail)
            elif doc_type == "design_doc":
                base += 0.08 * (concept_complex)
            elif doc_type == "report":
                base += 0.05 * concept_complex

            scores[doc_type] = max(0.0, min(1.0, base))

        best_type = max(scores, key=scores.get)
        sorted_scores = sorted(scores.values(), reverse=True)
        top = sorted_scores[0]
        second = sorted_scores[1] if len(sorted_scores) > 1 else 0.0
        margin = max(0.0, top - second)

        words = re.findall(r"[A-Za-z0-9_]+", content_lower)
        content_factor = min(1.0, len(words) / 200.0)

        base_conf = min(1.0, 0.5 + min(0.5, margin))
        confidence = max(0.1, round(base_conf * max(0.5, content_factor), 2))

        return best_type, confidence

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        weights = {"strong": 3.0, "medium": 2.0, "weak": 1.0}
        total_weight = 0.0
        max_possible = 0.0

        words = re.findall(r"[A-Za-z0-9_]+", content.lower())
        word_counts = Counter(words)
        content_len = max(100, len(words))

        for strength, terms in indicators.items():
            w = weights.get(strength, 1.0)
            max_possible += w * len(terms)
            for term in terms:
                if " " in term:
                    occurrences = len(re.findall(
                        r"\b" + re.escape(term.lower()) + r"\b", content, flags=re.IGNORECASE))
                else:
                    occurrences = word_counts[term.lower()]
                total_weight += w * min(occurrences, 3)

        freq_norm = total_weight / (max_possible * 3.0 + 1e-9)
        length_penalty = min(1.0, content_len / 300.0)

        score = max(0.0, min(1.0, 0.5 * freq_norm +
                    0.5 * length_penalty * freq_norm))
        return score

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        if not patterns:
            return 0.0
        matches = 0
        total = len(patterns)
        for pat in patterns:
            try:
                if re.search(pat, content, flags=re.IGNORECASE | re.MULTILINE):
                    matches += 1
            except re.error:
                continue
        ratio = matches / total
        return max(0.0, min(1.0, ratio))

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        text = content if content is not None else ""
        length = len(text)
        has_headers = bool(re.search(r"^\s*#{1,6}\s+\S", text, flags=re.MULTILINE)) or bool(
            re.search(r"^\s*(abstract|introduction|methods?|results?|discussion|conclusion|references)\s*$",
                      text, flags=re.IGNORECASE | re.MULTILINE)
        )
        has_steps = bool(re.search(r"(^\s*\d+\.\s)|(^\s*step\s*\d+)",
                         text, flags=re.IGNORECASE | re.MULTILINE))
        has_sections = bool(
            re.search(r"^\s*[A-Z][A-Za-z \-/]{2,}\s*$", text, flags=re.MULTILINE))
        has_code = "```" in text or bool(
            re.search(r"^\s{4,}\S", text, flags=re.MULTILINE))

        if doc_type == "api_reference":
            return "by_section_headers" if has_headers else "by_endpoints"
        if doc_type == "tutorial":
            return "by_steps" if has_steps else ("by_section_headers" if has_headers else "by_paragraphs")
        if doc_type == "research_paper":
            return "by_sections_abstract_intro_methods_results_discussion"
        if doc_type == "technical_spec":
            return "by_requirements_modules" if has_sections else "by_section_headers"
        if doc_type == "design_doc":
            return "by_components" if has_sections else "by_section_headers"
        if doc_type == "report":
            return "by_chapters" if length > 2000 else "by_section_headers"
        if doc_type == "blog_post":
            return "by_subheadings" if has_headers else "by_paragraphs"

        if has_headers:
            return "by_section_headers"
        if has_steps:
            return "by_steps"
        if has_code:
            return "by_code_blocks"
        return "by_paragraphs"

    def _calculate_algorithm_density(self, content: str) -> float:
        algo_terms = [
            "algorithm", "complexity", "runtime", "time complexity", "space complexity",
            "big-o", "big o", "o(n", "o(log n)", "o(n^2)", "np-hard", "np complete",
            "heuristic", "optimization", "greedy", "dynamic programming", "recurrence",
            "invariant", "proof", "correctness"
        ]
        words = re.findall(r"[A-Za-z0-9_]+", content.lower())
        if not words:
            return 0.0
        text = content.lower()
        count = 0
        for term in algo_terms:
            if " " in term or "(" in term or "-" in term:
                count += len(re.findall(re.escape(term), text))
            else:
                count += sum(1 for w in words if w == term)
        density = count / max(1, len(words))
        return max(0.0, min(1.0, density * 10.0))

    def _calculate_concept_complexity(self, content: str) -> float:
        words = re.findall(r"[A-Za-z]+", content.lower())
        if not words:
            return 0.0

        avg_word_len = sum(len(w) for w in words) / len(words)
        long_words = [w for w in words if len(w) >= 8]
        uniq_ratio = len(set(long_words)) / max(1, len(words))

        technical_affixes = ["tion", "sion", "ment", "ability",
                             "ization", "ality", "ology", "metric", "graphy"]
        affix_hits = sum(any(w.endswith(a) for a in technical_affixes)
                         for w in words) / len(words)

        score = (
            0.45 * min(1.0, avg_word_len / 8.0) +
            0.35 * min(1.0, uniq_ratio * 8.0) +
            0.20 * min(1.0, affix_hits * 5.0)
        )
        return max(0.0, min(1.0, score))

    def _calculate_implementation_detail_level(self, content: str) -> float:
        lines = content.splitlines()
        if not lines:
            return 0.0

        code_blocks = len(re.findall(r"```", content))
        indented_blocks = len(re.findall(
            r"^\s{4,}\S", content, flags=re.MULTILINE))
        function_like = len(re.findall(
            r"\b(def |class |function\s+\w+\(|\w+\s*\(.*\)\s*{?)", content))
        numbered_steps = len(re.findall(r"^\s*\d+\.\s", content, flags=re.MULTILINE)) + len(
            re.findall(r"^step\s*\d+", content,
                       flags=re.IGNORECASE | re.MULTILINE)
        )
        command_lines = len(re.findall(
            r"^\s*(\$ |curl |pip |npm |yarn |git )", content, flags=re.MULTILINE))
        code_fences = 1 if "```" in content else 0

        total_signals = (
            1.5 * code_blocks +
            1.0 * indented_blocks +
            1.0 * function_like +
            1.0 * numbered_steps +
            0.8 * command_lines +
            1.0 * code_fences
        )

        norm = total_signals / max(10.0, len(lines) / 20.0)
        return max(0.0, min(1.0, norm))
