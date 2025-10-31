from typing import Tuple, Dict, List
import re
import math


class DocumentAnalyzer:
    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        text = content or ""
        lower = text.lower()

        # Indicator dictionaries per doc type
        type_indicators: Dict[str, Dict[str, List[str]]] = {
            "research_paper": {
                "keywords": [
                    "abstract", "introduction", "related work", "method", "methodology", "experiment",
                    "results", "discussion", "conclusion", "future work", "references", "dataset",
                    "baseline", "evaluation", "proposed approach"
                ],
                "phrases": [
                    "we propose", "we present", "in this paper", "state-of-the-art", "our contributions",
                    "experimental results show", "significant improvement"
                ],
                "headers": [
                    "abstract", "introduction", "related work", "method", "methods", "methodology",
                    "experiments", "results", "discussion", "conclusion", "acknowledgements", "references"
                ],
                "regex": [
                    r"\b[A-Z][a-z]+ et al\.\s*\(\d{4}\)",
                    r"\[\d+\]",
                    r"\bO\([nN]?\^?.*?\)",
                    r"\bequation\s*\(\d+\)"
                ],
            },
            "tutorial": {
                "keywords": [
                    "step", "guide", "tutorial", "walkthrough", "beginner", "getting started",
                    "prerequisites", "summary", "tip", "note", "troubleshooting"
                ],
                "phrases": [
                    "in this tutorial", "follow these steps", "let's", "you will learn", "next,",
                    "first,", "second,", "finally,", "best practices"
                ],
                "headers": [
                    "prerequisites", "steps", "overview", "summary", "conclusion", "next steps"
                ],
                "regex": [
                    r"^\s*\d+\.\s",  # numbered steps
                    r"^\s*-\s",      # bullet points
                    r"```[\s\S]*?```"  # code blocks
                ],
            },
            "api_reference": {
                "keywords": [
                    "parameters", "returns", "response", "request", "status code", "endpoint",
                    "method", "default", "type", "throws", "deprecated", "authentication", "pagination"
                ],
                "phrases": [
                    "required", "optional", "path parameters", "query parameters", "request body",
                    "response body", "example request", "example response", "rate limit"
                ],
                "headers": [
                    "parameters", "returns", "examples", "authentication", "errors", "endpoints"
                ],
                "regex": [
                    r"GET\s+/[^\s]+", r"POST\s+/[^\s]+", r"PUT\s+/[^\s]+", r"DELETE\s+/[^\s]+",
                    r"^\s*def\s+\w+\(", r"\bclass\s+\w+\b", r"```(json|http|bash|python|js)?[\s\S]*?```"
                ],
            },
            "blog_post": {
                "keywords": [
                    "opinion", "insights", "story", "trend", "perspective", "takeaway", "overview",
                    "introduction", "conclusion", "thoughts", "why", "lessons"
                ],
                "phrases": [
                    "in my experience", "i think", "we believe", "here's why", "let's explore",
                    "key takeaways", "deep dive"
                ],
                "headers": [
                    "introduction", "overview", "conclusion", "key takeaways"
                ],
                "regex": [
                    r"^\s*-\s", r"^\s*\*\s", r"^\s*\d+\.\s"
                ],
            },
            "report": {
                "keywords": [
                    "executive summary", "findings", "analysis", "recommendations", "methodology",
                    "scope", "limitations", "results", "data", "metrics", "kpi", "appendix"
                ],
                "phrases": [
                    "this report", "we found", "our analysis indicates", "summary of findings",
                    "recommendations for", "based on data"
                ],
                "headers": [
                    "executive summary", "methodology", "findings", "results", "analysis",
                    "recommendations", "appendix"
                ],
                "regex": [
                    r"table\s+\d+",
                    r"figure\s+\d+",
                    r"\b\d+(\.\d+)?\s?%",
                    r"\b\d{1,3}(,\d{3})+(\.\d+)?\b"
                ],
            },
            "specification": {
                "keywords": [
                    "must", "shall", "should", "may", "requirements", "specification", "constraints",
                    "scope", "definitions", "compliance", "normative", "informative", "version"
                ],
                "phrases": [
                    "the system shall", "the client must", "is required to", "out of scope",
                    "backwards compatibility"
                ],
                "headers": [
                    "scope", "definitions", "requirements", "non-functional requirements",
                    "acceptance criteria", "compliance"
                ],
                "regex": [
                    r"\bRFC\s?\d+\b",
                    r"\b(section|clause)\s+\d+(\.\d+)*",
                    r"^\s*\[\w+-\d+\]\s"  # requirement id-like
                ],
            },
        }

        # Weighted scores
        scores: Dict[str, float] = {}
        for doc_type, indicators in type_indicators.items():
            score = self._calculate_weighted_score(lower, indicators)
            scores[doc_type] = score

        # Select best and compute confidence
        best_type = max(scores, key=scores.get) if scores else "unknown"
        best_score = scores.get(best_type, 0.0)
        # Normalize confidence against sum and max possible heuristic
        total = sum(scores.values()) + 1e-9
        rel = best_score / (total + 1e-9)
        # Also scale by a squashed absolute score
        abs_scale = 1 - math.exp(-best_score)
        confidence = max(0.05, min(0.99, 0.5 * rel + 0.5 * abs_scale))

        return best_type, float(round(confidence, 4)))

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        score = 0.0
        length_norm = max(500.0, float(len(content)))
        tokens = re.findall(r"[a-zA-Z0-9_#+\-/.]+", content)
        token_text = " " + " ".join(tokens) + " "
        lines = content.splitlines()

        def count_occurrences(hay: str, needle: str) -> int:
            return len(re.findall(re.escape(needle), hay))

        # Keywords weight
        for kw in indicators.get("keywords", []):
            # word boundary sensitive search
            if len(kw.split()) == 1:
                matches = len(re.findall(rf"\b{re.escape(kw)}\b", content))
            else:
                matches = count_occurrences(content, kw)
            if matches:
                score += 1.0 * min(matches, 10)

        # Phrases weight
        for ph in indicators.get("phrases", []):
            matches = count_occurrences(content, ph)
            if matches:
                score += 2.0 * min(matches, 6)

        # Headers weight
        header_set = set(h.strip().lower()
                         for h in indicators.get("headers", []))
        if header_set:
            header_hits = 0
            for line in lines:
                l = line.strip().lower().strip("#:-* ")
                if not l:
                    continue
                # Recognize typical header forms
                test = re.sub(r"^\d+(\.\d+)*\s*[:.)-]?\s*", "", l)
                if test in header_set or any(test.startswith(h + " ") for h in header_set):
                    header_hits += 1
            if header_hits:
                score += 2.5 * min(header_hits, 10)

        # Regex patterns weight
        regex_patterns = indicators.get("regex", [])
        if regex_patterns:
            regex_score = self._detect_pattern_score(content, regex_patterns)
            score += 3.0 * regex_score

        # Density bonus
        distinct_hits = 0
        for kw in set(indicators.get("keywords", [])):
            if re.search(rf"\b{re.escape(kw)}\b", content):
                distinct_hits += 1
        density_bonus = min(3.0, distinct_hits / 8.0)
        score += density_bonus

        # Normalize slightly by content length to avoid unfairly large docs
        scale = 1.0 + math.log10(length_norm / 500.0)
        return score / scale

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        if not patterns:
            return 0.0
        total_matches = 0
        for p in patterns:
            try:
                total_matches += len(re.findall(re.compile(p,
                                     re.MULTILINE), content))
            except re.error:
                continue
        # Normalize by content size (per 1000 chars) and cap
        norm = len(content) / 1000.0 + 1.0
        raw = total_matches / norm
        # squash to [0, ~]
        squashed = 1.0 - math.exp(-raw)
        return min(5.0, squashed * 5.0)

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        c = content or ""
        lower = c.lower()
        lines = c.splitlines()

        # Heading presence
        heading_lines = 0
        for ln in lines:
            s = ln.strip()
            if re.match(r"^#{1,6}\s+\S", s) or re.match(r"^\d+(\.\d+)*\s+\S", s):
                heading_lines += 1
            elif s and (s.endswith(":") and len(s.split()) <= 6):
                heading_lines += 1

        # Bullet/step density
        bullets = len([1 for ln in lines if re.match(r"^\s*[-*]\s+\S", ln)])
        steps = len([1 for ln in lines if re.match(r"^\s*\d+\.\s+\S", ln)])

        # Code presence
        code_blocks = len(re.findall(r"```[\s\S]*?```", c))
        inline_code = len(re.findall(r"`[^`]+`", c))
        code_density = self._calculate_implementation_detail_level(c)

        # Algorithmic/math density
        algo_density = self._calculate_algorithm_density(c)

        # Heuristic decisions by doc type and densities
        if doc_type == "api_reference":
            if code_blocks >= 1 or re.search(r"\b(GET|POST|PUT|DELETE)\s+/\S+", c):
                return "code_blocks"
            if heading_lines >= 3:
                return "section_based"
            return "paragraph"

        if doc_type == "tutorial":
            if steps >= 3 or bullets >= 5:
                if code_blocks >= 1:
                    return "hybrid"
                return "bullet_steps"
            if code_blocks >= 1 or code_density > 0.5:
                return "hybrid"
            return "paragraph"

        if doc_type == "research_paper":
            if heading_lines >= 3 or re.search(r"\babstract\b", lower):
                return "section_based"
            if algo_density > 0.4:
                return "section_based"
            return "paragraph"

        if doc_type == "report":
            if heading_lines >= 3:
                return "section_based"
            if bullets >= 5:
                return "bullet_steps"
            return "paragraph"

        if doc_type == "specification":
            if heading_lines >= 3:
                return "section_based"
            if bullets >= 5:
                return "bullet_steps"
            return "section_based"

        if doc_type == "blog_post":
            if bullets >= 5:
                return "bullet_steps"
            if code_blocks >= 1:
                return "hybrid"
            return "paragraph"

        # Fallback general heuristic
        if code_blocks >= 1:
            return "code_blocks"
        if heading_lines >= 3:
            return "section_based"
        if bullets + steps >= 5:
            return "bullet_steps"
        return "paragraph"

    def _calculate_algorithm_density(self, content: str) -> float:
        if not content:
            return 0.0
        lower = content.lower()

        indicators = [
            r"\btime complexity\b", r"\bspace complexity\b", r"\bO\([^)]+\)",
            r"\btheorem\b", r"\blemma\b", r"\bcorollary\b", r"\bproof\b",
            r"\balgorithm\b", r"\bpseudocode\b", r"\binvariant\b", r"\bconvergence\b",
            r"\bgradient\b", r"\bhessian\b", r"\boptimization\b", r"\bNP[-\s]?hard\b",
            r"\bNP[-\s]?complete\b", r"\blogic\b", r"\bentropy\b", r"\bvariance\b",
            r"\bexpected value\b", r"\bmarkov\b", r"\bmonte carlo\b", r"\bBayes\b",
            r"[Σ∑∏∞≈≃≅≡≤≥√→←↔±≠∈∉∩∪⊆⊂⊃∝∴∵∀∃∂∇λμσθπ]",
            r"[A-Z]\d?\s*=\s*.+",  # equation-like
        ]
        matches = 0
        for p in indicators:
            try:
                matches += len(re.findall(p, content))
            except re.error:
                continue

        words = max(1, len(re.findall(r"\b\w+\b", lower)))
        per_thousand = (matches / words) * 1000.0
        score = 1.0 - math.exp(-per_thousand / 5.0)
        return float(max(0.0, min(1.0, score)))

    def _calculate_concept_complexity(self, content: str) -> float:
        if not content:
            return 0.0
        text = content

        sentences = re.split(r"[.!?]+(?:\s+|$)", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = re.findall(r"\b\w+\b", text)
        word_count = max(1, len(words))

        avg_sentence_len = (word_count / max(1, len(sentences))
                            ) if sentences else len(words)
        avg_sentence_norm = min(1.0, avg_sentence_len / 30.0)

        complex_terms = [
            "asymptotic", "orthogonal", "stochastic", "nontrivial", "covariance", "manifold",
            "approximation", "differentiable", "isomorphic", "combinatorial", "heuristic",
            "regularization", "generalization", "spectral", "eigenvalue", "convergence",
            "nonlinear", "variational", "distributional", "transformer", "autoregressive",
            "bayesian", "likelihood", "prior", "posterior", "entropy", "dynamics",
        ]
        complex_hits = 0
        lower = text.lower()
        for term in complex_terms:
            complex_hits += len(re.findall(rf"\b{re.escape(term)}\b", lower))
        vocab = set(w.lower() for w in words)
        type_token_ratio = len(vocab) / word_count
        ttr_norm = min(1.0, type_token_ratio / 0.6)

        symbol_hits = len(re.findall(
            r"[Σ∑∏∞≈≃≅≡≤≥√→←↔±≠∈∉∩∪⊆⊂⊃∝∴∵∀∃∂∇λμσθπ]", text))
        symbol_norm = 1.0 - math.exp(-symbol_hits / 8.0)

        complex_norm = 1.0 - math.exp(-complex_hits / 8.0)

        score = 0.45 * avg_sentence_norm + 0.25 * ttr_norm + \
            0.15 * symbol_norm + 0.15 * complex_norm
        return float(max(0.0, min(1.0, score)))

    def _calculate_implementation_detail_level(self, content: str) -> float:
        if not content:
            return 0.0

        code_blocks = len(re.findall(r"```[\s\S]*?```", content))
        code_lines = len([1 for ln in content.splitlines() if re.match(
            r"\s*(def |class |for |while |if |else:|try:|catch|{|<\w+>|SELECT|INSERT|UPDATE|DELETE|#include)", ln)])
        inline_code = len(re.findall(r"`[^`]+`", content))
        api_style = len(re.findall(
            r"\b(GET|POST|PUT|DELETE|PATCH)\s+/\S+", content))
        signature_like = len(re.findall(
            r"\b\w+\s*\([^)]*\)\s*(->\s*\w+)?", content))
        param_blocks = len(re.findall(
            r"\b(parameters|args|arguments|returns|response|request)\b", content.lower()))

        raw = (
            3.0 * code_blocks +
            0.5 * code_lines +
            1.0 * inline_code +
            2.0 * api_style +
            0.2 * signature_like +
            1.0 * param_blocks
        )

        words = max(50, len(re.findall(r"\b\w+\b", content)))
        per_k = raw / (words / 200.0)  # relative to 200-word chunks
        score = 1.0 - math.exp(-per_k / 6.0)
        return float(max(0.0, min(1.0, score)))
