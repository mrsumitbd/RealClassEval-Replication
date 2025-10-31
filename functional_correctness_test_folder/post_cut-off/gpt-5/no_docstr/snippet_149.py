import re
import json
from typing import Optional, Dict, Tuple, List, Any
import pandas as pd

try:
    from openai import OpenAI
except Exception:  # ImportError or others if package not available
    OpenAI = None


class ArticleEvaluator:
    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4o'):
        self.api_key = openai_api_key
        self.model = model
        self.client = None
        if self.api_key and OpenAI is not None:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception:
                self.client = None

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        if not json_data or not title:
            return None

        # Common structures: {'articles': [{'title': ..., 'content': ...}, ...]}
        # or a dict keyed by title
        candidates = []

        if isinstance(json_data, dict):
            # Direct mapping by title
            for k, v in json_data.items():
                if isinstance(v, dict):
                    t = v.get('title') or v.get('name') or v.get('headline')
                    c = v.get('content') or v.get('body') or v.get('text')
                    if t and c:
                        candidates.append((t, c))
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            t = item.get('title') or item.get(
                                'name') or item.get('headline')
                            c = item.get('content') or item.get(
                                'body') or item.get('text')
                            if t and c:
                                candidates.append((t, c))

        # Exact match first (case-insensitive)
        lowered = title.strip().lower()
        for t, c in candidates:
            if t.strip().lower() == lowered:
                return c

        # Fallback: fuzzy contains
        for t, c in candidates:
            if lowered in t.strip().lower():
                return c

        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        cleaned = self._clean_text(article_content or "")
        sentences = self._split_sentences(cleaned)
        return cleaned, sentences

    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float = 0.2) -> Dict[str, Any]:
        if not reference_content or not generated_article:
            return {
                "overall_assessment": "Insufficient input to evaluate.",
                "accuracy_score": 0.0,
                "errors": [],
                "hallucinations": [],
                "missing_information": [],
                "supporting_quotes": []
            }

        prompt_system = (
            "You are a precise fact-checker. Compare the GENERATED_ARTICLE to the REFERENCE_CONTENT. "
            "Identify factual errors, unsupported claims (hallucinations), and missing key information. "
            "Return strictly valid JSON following the schema."
        )
        schema_description = {
            "type": "object",
            "properties": {
                "overall_assessment": {"type": "string"},
                "accuracy_score": {"type": "number"},
                "errors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "description": {"type": "string"},
                            "severity": {"type": "integer"},
                            "evidence": {"type": "string"},
                            "location": {"type": "string"}
                        },
                        "required": ["type", "description", "severity"]
                    }
                },
                "hallucinations": {"type": "array", "items": {"type": "string"}},
                "missing_information": {"type": "array", "items": {"type": "string"}},
                "supporting_quotes": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["overall_assessment", "errors", "hallucinations", "missing_information", "supporting_quotes"]
        }

        user_instructions = (
            "Schema:\n"
            + json.dumps(schema_description, ensure_ascii=False)
            + "\nGuidelines:\n"
            "- accuracy_score is from 0 to 100 (higher is better).\n"
            "- severity is integer 1 (minor) to 5 (critical).\n"
            "- errors list items should be specific factual inaccuracies.\n"
            "- hallucinations are unsupported or made-up claims.\n"
            "- missing_information are salient reference facts omitted in the generated article.\n"
            "Return only JSON."
        )

        content_block = (
            f"REFERENCE_CONTENT:\n{reference_content}\n\n"
            f"GENERATED_ARTICLE:\n{generated_article}\n"
        )

        result: Dict[str, Any] = {
            "overall_assessment": "",
            "accuracy_score": None,
            "errors": [],
            "hallucinations": [],
            "missing_information": [],
            "supporting_quotes": []
        }

        if self.client is None:
            # Offline fallback: simple heuristic diffing
            result["overall_assessment"] = "Heuristic evaluation due to unavailable model."
            result["supporting_quotes"] = []
            # Heuristic: missing key sentences from reference
            ref_sentences = set(self._split_sentences(
                self._clean_text(reference_content)))
            gen_sentences = set(self._split_sentences(
                self._clean_text(generated_article)))
            missing = [s for s in list(ref_sentences)
                       if s and s not in gen_sentences][:10]
            result["missing_information"] = missing

            # Heuristic hallucinations: sentences in generated not present in reference with named entities patterns
            hallucinations = []
            for s in list(gen_sentences):
                if s and s not in ref_sentences and re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4}|[A-Z][a-z]+ [A-Z][a-z]+)\b", s):
                    hallucinations.append(s)
            result["hallucinations"] = hallucinations[:10]

            # Heuristic errors not determinable; leave empty
            result["errors"] = []

            result["accuracy_score"] = self.calculate_accuracy_score(result)
            return result

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": user_instructions},
                    {"role": "user", "content": content_block}
                ]
            )
            text = ""
            try:
                text = (response.choices[0].message.content or "").strip()
            except Exception:
                text = ""
            parsed = self._parse_json_from_text(text)
            if not isinstance(parsed, dict):
                parsed = {}

            # Normalize fields
            result["overall_assessment"] = parsed.get("overall_assessment", "")
            result["accuracy_score"] = parsed.get("accuracy_score")
            result["errors"] = parsed.get("errors", []) or []
            result["hallucinations"] = parsed.get("hallucinations", []) or []
            result["missing_information"] = parsed.get(
                "missing_information", []) or []
            result["supporting_quotes"] = parsed.get(
                "supporting_quotes", []) or []

            # Validate types
            if not isinstance(result["errors"], list):
                result["errors"] = []
            if not isinstance(result["hallucinations"], list):
                result["hallucinations"] = []
            if not isinstance(result["missing_information"], list):
                result["missing_information"] = []
            if not isinstance(result["supporting_quotes"], list):
                result["supporting_quotes"] = []

            # Ensure severities are ints within 1..5
            normalized_errors = []
            for e in result["errors"]:
                if not isinstance(e, dict):
                    continue
                sev = e.get("severity", 3)
                try:
                    sev = int(sev)
                except Exception:
                    sev = 3
                sev = max(1, min(5, sev))
                normalized_errors.append({
                    "type": e.get("type", "unspecified"),
                    "description": e.get("description", ""),
                    "severity": sev,
                    "evidence": e.get("evidence", ""),
                    "location": e.get("location", "")
                })
            result["errors"] = normalized_errors

            if result.get("accuracy_score") is None:
                result["accuracy_score"] = self.calculate_accuracy_score(
                    result)

            return result
        except Exception:
            # If API fails, fallback heuristic
            result["overall_assessment"] = "Heuristic evaluation due to API failure."
            ref_sentences = set(self._split_sentences(
                self._clean_text(reference_content)))
            gen_sentences = set(self._split_sentences(
                self._clean_text(generated_article)))
            missing = [s for s in list(ref_sentences)
                       if s and s not in gen_sentences][:10]
            result["missing_information"] = missing
            hallucinations = []
            for s in list(gen_sentences):
                if s and s not in ref_sentences and re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4}|[A-Z][a-z]+ [A-Z][a-z]+)\b", s):
                    hallucinations.append(s)
            result["hallucinations"] = hallucinations[:10]
            result["errors"] = []
            result["accuracy_score"] = self.calculate_accuracy_score(result)
            return result

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        if not isinstance(evaluation_data, dict):
            return 0.0
        if "accuracy_score" in evaluation_data and isinstance(evaluation_data["accuracy_score"], (int, float)):
            score = float(evaluation_data["accuracy_score"])
            return max(0.0, min(100.0, score))

        base = 100.0
        errors = evaluation_data.get("errors", []) or []
        hallucinations = evaluation_data.get("hallucinations", []) or []
        missing_info = evaluation_data.get("missing_information", []) or []

        penalty = 0.0
        for e in errors:
            sev = 3
            if isinstance(e, dict):
                sev = int(e.get("severity", 3)) if str(
                    e.get("severity", "")).isdigit() else 3
            penalty += 8.0 * max(1, min(5, sev))
        penalty += 10.0 * len(hallucinations)
        penalty += 5.0 * len(missing_info)

        score = base - penalty
        return max(0.0, min(100.0, score))

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        stats = {
            "total_errors": 0,
            "avg_severity": 0.0,
            "errors_by_type": {},
            "hallucination_count": 0,
            "missing_info_count": 0,
            "calculated_score": None
        }
        if not isinstance(evaluation_data, dict):
            return stats

        errors = evaluation_data.get("errors", []) or []
        stats["total_errors"] = len(errors)
        if errors:
            severities = []
            for e in errors:
                sev = 3
                if isinstance(e, dict):
                    try:
                        sev = int(e.get("severity", 3))
                    except Exception:
                        sev = 3
                severities.append(max(1, min(5, sev)))
                etype = (e.get("type", "unspecified") if isinstance(
                    e, dict) else "unspecified") or "unspecified"
                stats["errors_by_type"][etype] = stats["errors_by_type"].get(
                    etype, 0) + 1
            stats["avg_severity"] = sum(severities) / len(severities)
        else:
            stats["avg_severity"] = 0.0

        stats["hallucination_count"] = len(
            evaluation_data.get("hallucinations", []) or [])
        stats["missing_info_count"] = len(
            evaluation_data.get("missing_information", []) or [])
        stats["calculated_score"] = self.calculate_accuracy_score(
            evaluation_data)
        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        rows: List[Dict[str, Any]] = []
        if not isinstance(evaluation_data, dict):
            return pd.DataFrame(rows)

        overall = evaluation_data.get("overall_assessment", "")
        score = evaluation_data.get(
            "accuracy_score", self.calculate_accuracy_score(evaluation_data))

        # Errors
        for e in evaluation_data.get("errors", []) or []:
            if not isinstance(e, dict):
                continue
            rows.append({
                "category": "error",
                "type": e.get("type", "unspecified"),
                "description": e.get("description", ""),
                "severity": e.get("severity", None),
                "evidence": e.get("evidence", ""),
                "location": e.get("location", ""),
                "overall_assessment": overall,
                "accuracy_score": score
            })

        # Hallucinations
        for h in evaluation_data.get("hallucinations", []) or []:
            rows.append({
                "category": "hallucination",
                "type": "hallucination",
                "description": h,
                "severity": None,
                "evidence": "",
                "location": "",
                "overall_assessment": overall,
                "accuracy_score": score
            })

        # Missing information
        for m in evaluation_data.get("missing_information", []) or []:
            rows.append({
                "category": "missing_information",
                "type": "missing_information",
                "description": m,
                "severity": None,
                "evidence": "",
                "location": "",
                "overall_assessment": overall,
                "accuracy_score": score
            })

        if not rows:
            # Provide a single summary row if no detailed items
            rows.append({
                "category": "summary",
                "type": "",
                "description": "",
                "severity": None,
                "evidence": "",
                "location": "",
                "overall_assessment": overall,
                "accuracy_score": score
            })

        return pd.DataFrame(rows)

    def _clean_text(self, text: str) -> str:
        text = text or ""
        text = re.sub(r"\r\n?", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _split_sentences(self, text: str) -> List[str]:
        if not text:
            return []
        # Simple sentence splitter
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text)
        sentences = []
        for p in parts:
            s = p.strip()
            if s:
                sentences.append(s)
        return sentences

    def _parse_json_from_text(self, text: str) -> Any:
        if not text:
            return {}
        text = text.strip()
        # Direct JSON
        try:
            return json.loads(text)
        except Exception:
            pass

        # Extract JSON block between braces
        try:
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                candidate = text[start:end + 1]
                return json.loads(candidate)
        except Exception:
            pass

        # Fix common trailing commas
        candidate = re.sub(r",\s*([}\]])", r"\1", text)
        try:
            return json.loads(candidate)
        except Exception:
            return {}
