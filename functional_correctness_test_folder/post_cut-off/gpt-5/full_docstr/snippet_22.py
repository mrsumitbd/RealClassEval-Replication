from typing import Tuple, Dict, List
import re
from collections import Counter


class DocumentAnalyzer:
    '''Enhanced document analyzer using semantic content analysis instead of mechanical structure detection'''

    def analyze_document_type(self, content: str) -> Tuple[str, float]:
        '''
        Enhanced document type analysis based on semantic content patterns
        Returns:
            Tuple[str, float]: (document_type, confidence_score)
        '''
        text = content.lower()
        doc_indicators: Dict[str, Dict[str, List[str]]] = {
            "research_paper": {
                "strong": [
                    "abstract", "introduction", "methodology", "methods", "results", "discussion",
                    "conclusion", "references", "related work", "literature review", "dataset",
                    "experimental setup", "evaluation", "we propose", "we present", "contribution",
                    "state-of-the-art", "baseline", "significant improvement", "hypothesis",
                    "statistically significant", "theorem", "lemma", "proof", "complexity o("
                ],
                "medium": [
                    "model", "architecture", "algorithm", "dataset", "benchmark",
                    "in this paper", "empirical", "quantitative", "qualitative"
                ],
                "weak": [
                    "future work", "appendix", "footnote", "supplementary"
                ],
            },
            "tutorial": {
                "strong": [
                    "step-by-step", "follow along", "in this tutorial", "you will learn", "let's build",
                    "prerequisites", "requirements", "step 1", "step 2", "step 3", "walkthrough",
                    "hands-on", "try it", "exercise", "practice", "demo"
                ],
                "medium": [
                    "how to", "guide", "getting started", "cookbook", "tips", "tricks",
                    "common mistakes", "best practices"
                ],
                "weak": [
                    "code snippet", "sample code", "example output", "screenshot"
                ],
            },
            "technical_spec": {
                "strong": [
                    "specification", "shall", "must", "should", "requirement", "constraints",
                    "scope", "definitions", "terminology", "conformance", "compliance",
                    "non-normative", "normative", "protocol", "message format", "field", "bitmask",
                    "rfc", "ietf", "draft", "versioning"
                ],
                "medium": [
                    "implementation notes", "backwards compatibility", "interop", "security considerations",
                    "error codes", "status codes"
                ],
                "weak": [
                    "appendix a", "appendix b", "glossary"
                ],
            },
            "api_reference": {
                "strong": [
                    "endpoint", "endpoints", "request", "response", "parameter", "parameters",
                    "query", "path", "json", "xml", "schema", "http", "status code", "authentication",
                    "authorization", "curl", "example request", "example response",
                    "rate limit", "pagination", "base url"
                ],
                "medium": [
                    "sdk", "client", "resource", "method", "get", "post", "put", "delete",
                    "content-type", "headers", "bearer", "token"
                ],
                "weak": [
                    "deprecated", "beta", "changelog"
                ],
            },
            "blog_post": {
                "strong": [
                    "opinions", "insights", "story", "journey", "thoughts", "my experience",
                    "lessons learned", "why we", "behind the scenes"
                ],
                "medium": [
                    "introduction", "conclusion", "summary", "overview", "insight",
                    "hot take", "trend", "perspective"
                ],
                "weak": [
                    "comments", "subscribe", "share this", "newsletter"
                ],
            },
            "whitepaper": {
                "strong": [
                    "executive summary", "industry", "market", "solution", "problem statement",
                    "business value", "roi", "stakeholders", "benefits", "case example",
                    "reference architecture"
                ],
                "medium": [
                    "overview", "recommendations", "roadmap", "implementation approach", "risk",
                    "mitigation", "cost"
                ],
                "weak": [
                    "appendix", "glossary", "acknowledgements"
                ],
            },
            "case_study": {
                "strong": [
                    "client", "challenge", "solution", "outcome", "results", "impact",
                    "before and after", "metrics achieved", "success story"
                ],
                "medium": [
                    "industry", "timeline", "budget", "stakeholder", "kpi"
                ],
                "weak": [
                    "testimonial", "quote"
                ],
            },
            "news_article": {
                "strong": [
                    "according to", "reported", "announced", "breaking", "statement", "official",
                    "spokesperson", "press release", "exclusive"
                ],
                "medium": [
                    "sources say", "investigation", "interview", "covering", "update"
                ],
                "weak": [
                    "photo", "caption", "byline", "editor", "op-ed"
                ],
            },
        }

        # Weighted scoring per doc type
        type_scores: Dict[str, float] = {}
        for dtype, indicators in doc_indicators.items():
            type_scores[dtype] = self._calculate_weighted_score(
                text, indicators)

        if not type_scores:
            return ("unknown", 0.0)

        best_type = max(type_scores, key=type_scores.get)
        best_score = type_scores[best_type]
        # Confidence calibrated relative to runner-up to avoid overconfidence
        sorted_scores = sorted(type_scores.values(), reverse=True)
        runner_up = sorted_scores[1] if len(sorted_scores) > 1 else 0.0
        margin = max(best_score - runner_up, 0.0)

        # Aggregate confidence: blend absolute signal and margin
        confidence = max(0.0, min(1.0, 0.6 * best_score +
                         0.4 * (margin if best_score > 0 else 0.0)))
        return (best_type, confidence)

    def _calculate_weighted_score(self, content: str, indicators: Dict[str, List[str]]) -> float:
        '''Calculate weighted semantic indicator scores'''
        weights = {"strong": 1.0, "medium": 0.6, "weak": 0.3}
        total_weighted = 0.0
        total_possible = 0.0
        for strength, patterns in indicators.items():
            weight = weights.get(strength, 0.3)
            score = self._detect_pattern_score(content, patterns)
            total_weighted += score * weight
            total_possible += 1.0 * weight  # normalize by weight tiers

        if total_possible == 0:
            return 0.0

        # Normalize to 0..1
        normalized = total_weighted / total_possible
        return max(0.0, min(1.0, normalized))

    def _detect_pattern_score(self, content: str, patterns: List[str]) -> float:
        '''Detect semantic pattern matching scores'''
        if not patterns:
            return 0.0

        text = content.lower()
        max_per_pattern = 3  # cap to reduce repetition bias
        total_hits = 0
        total_cap = len(patterns) * max_per_pattern

        # Boost patterns appearing early (intro) or as headings
        intro_window = text[:800]
        # Heading-like lines
        heading_lines = [ln.strip() for ln in content.splitlines()
                         if ln.strip() and len(ln) < 120]
        heading_blob = ("\n".join(heading_lines)).lower()

        for pat in patterns:
            p = pat.lower().strip()
            if not p:
                continue

            # Basic occurrence count
            count = len(re.findall(re.escape(p), text))
            count = min(count, max_per_pattern)

            # Early/heading boost
            boost = 0
            if p in intro_window:
                boost += 1
            if p in heading_blob:
                boost += 1

            total_hits += min(max_per_pattern, count + boost)

        if total_cap == 0:
            return 0.0

        return max(0.0, min(1.0, total_hits / total_cap))

    def detect_segmentation_strategy(self, content: str, doc_type: str) -> str:
        '''
        Intelligently determine the best segmentation strategy based on content semantics rather than mechanical structure
        '''
        text = content.lower()
        algo_density = self._calculate_algorithm_density(text)
        concept_complexity = self._calculate_concept_complexity(text)
        impl_detail = self._calculate_implementation_detail_level(text)

        code_like = impl_detail > 0.55
        highly_algorithmic = algo_density > 0.5
        complex_concepts = concept_complexity > 0.55

        if doc_type == "api_reference" or ("endpoint" in text and "request" in text and "response" in text):
            return "by_api_endpoints"
        if doc_type == "technical_spec":
            return "by_section_headings" if complex_concepts else "by_semantic_topics"
        if doc_type == "research_paper":
            if highly_algorithmic:
                return "by_algorithms"
            return "by_section_headings"
        if doc_type == "tutorial":
            return "hybrid" if code_like else "by_semantic_topics"
        if doc_type == "whitepaper":
            return "by_section_headings" if complex_concepts else "by_semantic_topics"
        if doc_type == "case_study":
            return "by_use_cases"
        if doc_type == "blog_post":
            return "by_paragraph"
        if doc_type == "news_article":
            return "by_paragraph"

        # Fallbacks based on metrics
        if code_like:
            if "curl" in text or "http" in text or "status code" in text:
                return "by_api_endpoints"
            return "by_code_blocks"
        if highly_algorithmic:
            return "by_algorithms"
        if complex_concepts:
            return "by_section_headings"
        return "by_semantic_topics"

    def _calculate_algorithm_density(self, content: str) -> float:
        '''Calculate algorithm content density'''
        algo_terms = [
            "algorithm", "time complexity", "space complexity", "o(", "o(n", "o(log", "o(n^",
            "pseudo-code", "pseudocode", "step", "iterate", "initialize", "loop", "recurrence",
            "dynamic programming", "greedy", "divide and conquer", "proof", "theorem", "lemma",
            "corollary", "invariant"
        ]
        # Add code fence as a light proxy for algorithm blocks
        code_fences = len(re.findall(r"```|<code>|</code>", content))

        base_hits = 0
        for term in algo_terms:
            base_hits += len(re.findall(re.escape(term), content))

        # Length normalization
        word_count = max(50, len(re.findall(r"\b\w+\b", content)))
        density = (base_hits * 1.0 + code_fences * 1.5) / word_count

        return max(0.0, min(1.0, density * 5.0))  # scale into 0..1

    def _calculate_concept_complexity(self, content: str) -> float:
        '''Calculate concept complexity'''
        sentences = re.split(r"[.!?]\s+", content)
        sentences = [s for s in sentences if s.strip()]
        if not sentences:
            return 0.0

        # Average sentence length
        sent_lengths = [len(re.findall(r"\b\w+\b", s)) for s in sentences]
        avg_len = sum(sent_lengths) / max(1, len(sent_lengths))

        # Technical term richness
        tech_terms = [
            "architecture", "protocol", "consistency", "convergence", "abstraction", "synchronization",
            "latency", "throughput", "scalability", "idempotent", "isomorphic", "homomorphism",
            "serialization", "availability", "partition", "consensus", "metric", "optimization",
            "probabilistic", "deterministic", "stochastic", "gradient", "regularization", "manifold",
            "topology", "semantics", "ontology", "axiom", "categorical", "combinatorial",
            "approximation", "bounded", "constraint", "inference", "loss function"
        ]
        unique_words = set(re.findall(r"\b\w+\b", content))
        tech_hits = sum(1 for t in tech_terms if t in unique_words)

        # Normalize components
        # 28 words per sentence is complex
        len_component = min(avg_len / 28.0, 1.0)
        vocab_component = min(tech_hits / 12.0, 1.0)

        # Blend and cap
        complexity = 0.6 * len_component + 0.4 * vocab_component
        return max(0.0, min(1.0, complexity))

    def _calculate_implementation_detail_level(self, content: str) -> float:
        '''Calculate implementation detail level'''
        code_markers = [
            "def ", "class ", "public ", "private ", "protected ", "static ", "void ",
            "int ", "string ", "boolean ", "{", "}", ";", "=>", "::", "import ", "using ",
            "#include", "printf(", "console.log", "var ", "let ", "const ", "fn ", "lambda",
            "param", "parameter", "returns", "example", "code", "snippet"
        ]
        api_markers = [
            "endpoint", "request", "response", "parameter", "status code", "http", "curl",
            "header", "authentication", "authorization", "token", "payload", "schema", "json"
        ]

        code_hits = sum(len(re.findall(re.escape(t), content))
                        for t in code_markers)
        api_hits = sum(len(re.findall(re.escape(t), content))
                       for t in api_markers)
        fence_hits = len(re.findall(r"```|~~~|<code>|</code>", content))

        word_count = max(50, len(re.findall(r"\b\w+\b", content)))
        raw = (code_hits * 1.0 + api_hits * 1.2 +
               fence_hits * 2.0) / word_count

        return max(0.0, min(1.0, raw * 6.0))
