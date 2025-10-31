import os
import json
import re
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


class ArticleEvaluator:
    '''
    A class to evaluate the factual accuracy of AI-generated Wikipedia articles
    against reference articles using OpenAI models.
    '''

    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4o'):
        '''
        Initialize the ArticleEvaluator with API credentials and model settings.
        Args:
            openai_api_key: API key for OpenAI (falls back to OPENAI_API_KEY env var)
            model: The OpenAI model to use for evaluation (default: gpt-4o)
        '''
        self.api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self._client = None
        self._openai_import_error = None
        try:
            from openai import OpenAI  # type: ignore
            if self.api_key:
                self._client = OpenAI(api_key=self.api_key)
            else:
                # Instantiate without api_key; OpenAI SDK will read from env if present
                self._client = OpenAI()
        except Exception as e:
            self._openai_import_error = e
            self._client = None

    def _ensure_client(self):
        if self._client is not None:
            return
        if self._openai_import_error is not None:
            raise RuntimeError(
                f"OpenAI SDK not available: {self._openai_import_error}")
        try:
            from openai import OpenAI  # type: ignore
            if self.api_key:
                self._client = OpenAI(api_key=self.api_key)
            else:
                self._client = OpenAI()
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize OpenAI client: {e}") from e

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        '''
        Retrieve reference article text from the JSON data.
        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve
        Returns:
            The plain text content of the reference article, or None if not found
        '''
        def extract_text(obj: Dict) -> Optional[str]:
            # Common fields for text content
            for key in ['plain_text', 'text', 'content', 'body']:
                if key in obj and isinstance(obj[key], str) and obj[key].strip():
                    return obj[key]
            # Sections-based content
            if 'sections' in obj and isinstance(obj['sections'], list):
                parts: List[str] = []
                for sec in obj['sections']:
                    if isinstance(sec, dict):
                        if 'text' in sec and isinstance(sec['text'], str):
                            parts.append(sec['text'])
                        elif 'content' in sec and isinstance(sec['content'], str):
                            parts.append(sec['content'])
                if parts:
                    return "\n\n".join(parts)
            # Revision or extract fields (common in some Wikipedia datasets)
            if 'extract' in obj and isinstance(obj['extract'], str):
                return obj['extract']
            if 'revisions' in obj and isinstance(obj['revisions'], list):
                for rev in obj['revisions']:
                    if isinstance(rev, dict) and 'content' in rev and isinstance(rev['content'], str):
                        return rev['content']
            return None

        def matches_title(obj: Dict, target: str) -> bool:
            t = obj.get('title') or obj.get('name') or obj.get('page_title')
            return isinstance(t, str) and t.strip().lower() == target.strip().lower()

        candidates: List[Dict] = []
        if isinstance(json_data, list):
            candidates = [x for x in json_data if isinstance(x, dict)]
        elif isinstance(json_data, dict):
            # try common container keys
            for key in ['articles', 'pages', 'entries', 'items', 'docs', 'documents', 'data', 'results']:
                if key in json_data and isinstance(json_data[key], list):
                    candidates.extend(
                        [x for x in json_data[key] if isinstance(x, dict)])
            # Top-level single article possibility
            if not candidates and 'title' in json_data:
                candidates.append(json_data)

        # First try exact title match
        for obj in candidates:
            if matches_title(obj, title):
                text = extract_text(obj)
                if text:
                    return text

        # If exact match not found, try case-insensitive contains
        lowered = title.strip().lower()
        for obj in candidates:
            t = (obj.get('title') or obj.get('name')
                 or obj.get('page_title') or '')
            if isinstance(t, str) and lowered in t.lower():
                text = extract_text(obj)
                if text:
                    return text

        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        '''
        Prepare an AI-generated article for evaluation by numbering its lines.
        Args:
            article_content: The content of the AI-generated article
        Returns:
            A tuple containing:
            - Numbered article text suitable for the prompt
            - List of the original lines for further processing
        '''
        if article_content is None:
            article_content = ""
        # Normalize line breaks and split
        raw_lines = [ln.rstrip() for ln in article_content.replace(
            '\r\n', '\n').replace('\r', '\n').split('\n')]
        # Keep original lines for reassembly; filter out empty lines for evaluation numbering to avoid noise
        non_empty_lines = [ln for ln in raw_lines if ln.strip() != ""]
        numbered_lines = [f"{i+1}. {line}" for i,
                          line in enumerate(non_empty_lines)]
        numbered_text = "\n".join(numbered_lines)
        return numbered_text, non_empty_lines

    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float = 0.2) -> Dict[str, Any]:
        '''
        Evaluate the factual accuracy of an AI-generated article against a reference.
        Args:
            reference_content: The text of the reference Wikipedia article
            generated_article: The text of the AI-generated article
            temperature: The sampling temperature for the OpenAI API call
        Returns:
            Dictionary containing the evaluation results
        '''
        self._ensure_client()

        numbered_text, original_lines = self.prepare_article_for_evaluation(
            generated_article)

        system_prompt = (
            "You are a meticulous fact-checker for Wikipedia articles. "
            "Compare each numbered line of the AI-generated article to the provided reference article. "
            "Decide for each line whether it is: 'correct', 'partially_correct', 'incorrect', or 'unsupported'. "
            "'unsupported' means the claim is not present or verifiable in the reference. "
            "Provide a brief rationale. If a line is not fully correct, propose a concise suggested_correction "
            "based solely on the reference content. "
            "Respond ONLY with a strict JSON object."
        )

        user_prompt = (
            "REFERENCE ARTICLE:\n"
            "------------------\n"
            f"{reference_content}\n\n"
            "AI-GENERATED ARTICLE (NUMBERED LINES):\n"
            "--------------------------------------\n"
            f"{numbered_text}\n\n"
            "Output JSON schema:\n"
            "{\n"
            '  "overall_assessment": "string concise summary",\n'
            '  "line_evaluations": [\n'
            "    {\n"
            '      "line_number": int,\n'
            '      "text": "original line text",\n'
            '      "verdict": "correct|partially_correct|incorrect|unsupported",\n'
            '      "rationale": "brief explanation",\n'
            '      "suggested_correction": "string optional when not correct"\n'
            "    }\n"
            "  ]\n"
            "}\n"
            "Ensure one entry per numbered line, in order."
        )

        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            content = resp.choices[0].message.content if resp and resp.choices else ""
        except Exception as e:
            return {
                "error": f"OpenAI API error: {e}",
                "overall_assessment": "",
                "line_evaluations": [],
                "raw_response": None,
            }

        parsed: Dict[str, Any] = {}
        if content:
            try:
                parsed = json.loads(content)
            except Exception:
                # Try to extract the first JSON object
                match = re.search(r'\{.*\}', content, flags=re.DOTALL)
                if match:
                    try:
                        parsed = json.loads(match.group(0))
                    except Exception:
                        parsed = {}
        if not parsed:
            parsed = {}

        line_evals = parsed.get("line_evaluations")
        if not isinstance(line_evals, list):
            # Fallback: reconstruct from original lines with unknown verdicts
            line_evals = []

        # Ensure one evaluation per line; repair/infer missing fields
        repaired: List[Dict[str, Any]] = []
        for idx, line_text in enumerate(original_lines, start=1):
            existing = None
            # Try to find a matching evaluation by line_number
            if line_evals:
                for ev in line_evals:
                    if isinstance(ev, dict) and ev.get("line_number") == idx:
                        existing = ev
                        break
                # If not found by number, try position-based
                if existing is None and idx - 1 < len(line_evals) and isinstance(line_evals[idx - 1], dict):
                    existing = line_evals[idx - 1]

            if not isinstance(existing, dict):
                existing = {}

            verdict = existing.get("verdict")
            if verdict not in {"correct", "partially_correct", "incorrect", "unsupported"}:
                verdict = "unsupported"

            repaired.append({
                "line_number": idx,
                "text": line_text,
                "verdict": verdict,
                "rationale": existing.get("rationale", ""),
                "suggested_correction": existing.get("suggested_correction", None),
            })

        result = {
            "overall_assessment": parsed.get("overall_assessment", ""),
            "line_evaluations": repaired,
            "raw_response": content,
        }
        return result

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        lines: List[Dict[str, Any]] = evaluation_data.get(
            "line_evaluations", [])
        if not lines:
            return 0.0
        total = len(lines)
        score_sum = 0.0
        for ev in lines:
            verdict = (ev or {}).get("verdict")
            if verdict == "correct":
                score_sum += 1.0
            elif verdict == "partially_correct":
                score_sum += 0.5
            elif verdict in {"incorrect", "unsupported"}:
                score_sum += 0.0
            else:
                score_sum += 0.0
        ratio = score_sum / total if total > 0 else 0.0
        return 2.0 * ratio - 1.0

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        lines: List[Dict[str, Any]] = evaluation_data.get(
            "line_evaluations", [])
        stats = {
            "total_lines": 0,
            "correct": 0,
            "partially_correct": 0,
            "incorrect": 0,
            "unsupported": 0,
            "accuracy_ratio": 0.0,
            "normalized_score": 0.0,
        }
        if not lines:
            return stats

        stats["total_lines"] = len(lines)
        for ev in lines:
            verdict = (ev or {}).get("verdict")
            if verdict in stats:
                stats[verdict] += 1
            elif verdict == "partially_correct":
                stats["partially_correct"] += 1
            elif verdict == "correct":
                stats["correct"] += 1
            elif verdict == "incorrect":
                stats["incorrect"] += 1
            elif verdict == "unsupported":
                stats["unsupported"] += 1

        # Weighted accuracy: correct=1, partially_correct=0.5
        weighted = stats["correct"] + 0.5 * stats["partially_correct"]
        stats["accuracy_ratio"] = weighted / \
            stats["total_lines"] if stats["total_lines"] > 0 else 0.0
        stats["normalized_score"] = 2.0 * stats["accuracy_ratio"] - 1.0
        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        lines: List[Dict[str, Any]] = evaluation_data.get(
            "line_evaluations", [])
        rows: List[Dict[str, Any]] = []
        for ev in lines:
            if not isinstance(ev, dict):
                continue
            rows.append({
                "line_number": ev.get("line_number"),
                "text": ev.get("text"),
                "verdict": ev.get("verdict"),
                "rationale": ev.get("rationale"),
                "suggested_correction": ev.get("suggested_correction"),
            })
        df = pd.DataFrame(rows, columns=[
                          "line_number", "text", "verdict", "rationale", "suggested_correction"])
        return df
