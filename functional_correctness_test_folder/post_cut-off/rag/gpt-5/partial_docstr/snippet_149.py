import os
import re
import json
from typing import Optional, List, Dict, Tuple, Any

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
        self.api_key = openai_api_key or os.environ.get('OPENAI_API_KEY')
        self.model = model
        self._client = None
        self._use_v1_client = False  # True if using from openai import OpenAI client

    def _ensure_client(self):
        if self._client is not None:
            return
        # Try new-style client first
        try:
            from openai import OpenAI  # type: ignore
            self._client = OpenAI(
                api_key=self.api_key) if self.api_key else OpenAI()
            self._use_v1_client = True
            return
        except Exception:
            pass
        # Fallback to legacy openai module
        try:
            import openai  # type: ignore
            if self.api_key:
                openai.api_key = self.api_key
            self._client = openai
            self._use_v1_client = False
        except Exception as e:
            raise RuntimeError(
                "Failed to initialize OpenAI client. Ensure 'openai' package is installed.") from e

    def _call_openai(self, messages: List[Dict[str, str]], temperature: float) -> str:
        self._ensure_client()
        # Try chat.completions (new and old)
        try:
            if self._use_v1_client:
                resp = self._client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature
                )
                return resp.choices[0].message.content  # type: ignore
            else:
                # Legacy API
                resp = self._client.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature
                )
                return resp.choices[0].message["content"]  # type: ignore
        except Exception:
            # Try responses endpoint if available
            try:
                resp = self._client.responses.create(  # type: ignore
                    model=self.model,
                    input=messages,
                    temperature=temperature
                )
                # Attempt to extract text
                if hasattr(resp, "output_text"):
                    return resp.output_text  # type: ignore
                # Fallback generic extraction
                if hasattr(resp, "output") and isinstance(resp.output, list) and resp.output:
                    first = resp.output[0]
                    if isinstance(first, dict) and "content" in first:
                        return str(first["content"])
                return json.dumps(resp)  # type: ignore
            except Exception as e:
                raise RuntimeError(f"OpenAI API call failed: {e}") from e

    def _extract_text_from_article_obj(self, article_obj: Any) -> Optional[str]:
        # Direct string
        if isinstance(article_obj, str):
            return article_obj.strip() if article_obj.strip() else None

        if not isinstance(article_obj, dict):
            return None

        # Common fields
        for key in ["text", "content", "body", "article_text", "plain_text"]:
            if isinstance(article_obj.get(key), str) and article_obj.get(key).strip():
                return article_obj.get(key).strip()

        # Sections-based
        sections = article_obj.get("sections") or article_obj.get(
            "paragraphs") or article_obj.get("chunks")
        if isinstance(sections, list):
            parts: List[str] = []
            for sec in sections:
                if isinstance(sec, str):
                    parts.append(sec)
                elif isinstance(sec, dict):
                    for key in ["text", "content", "body"]:
                        if isinstance(sec.get(key), str):
                            parts.append(sec.get(key))
            text = "\n\n".join(
                [p.strip() for p in parts if isinstance(p, str) and p.strip()])
            if text.strip():
                return text.strip()

        # Nested content
        if "page" in article_obj and isinstance(article_obj["page"], dict):
            return self._extract_text_from_article_obj(article_obj["page"])

        return None

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        '''
        Retrieve reference article text from the JSON data.
        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve
        Returns:
            The plain text content of the reference article, or None if not found
        '''
        if not json_data or not title:
            return None

        title_norm = title.strip().lower()

        # If dict mapping titles -> article objects or text
        if isinstance(json_data, dict):
            # Direct key match
            for k, v in json_data.items():
                if isinstance(k, str) and k.strip().lower() == title_norm:
                    return self._extract_text_from_article_obj(v)

            # Look for container keys
            for container_key in ["articles", "documents", "pages", "items", "data"]:
                container = json_data.get(container_key)
                if isinstance(container, list):
                    for item in container:
                        if isinstance(item, dict):
                            item_title = item.get("title") or item.get(
                                "name") or item.get("id")
                            if isinstance(item_title, str) and item_title.strip().lower() == title_norm:
                                found = self._extract_text_from_article_obj(
                                    item)
                                if found:
                                    return found

        # If list of articles
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    item_title = item.get("title") or item.get(
                        "name") or item.get("id")
                    if isinstance(item_title, str) and item_title.strip().lower() == title_norm:
                        found = self._extract_text_from_article_obj(item)
                        if found:
                            return found

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
        # Normalize newlines, trim trailing spaces
        raw_lines = [ln.rstrip() for ln in article_content.replace(
            "\r\n", "\n").replace("\r", "\n").split("\n")]
        # Keep non-empty and also collapse multiple spaces inside nothing
        lines = [ln for ln in raw_lines if ln.strip() != ""]
        numbered = "\n".join(f"{i+1}. {line}" for i, line in enumerate(lines))
        return numbered, lines

    def _build_prompt(self, reference_content: str, numbered_generated: str) -> List[Dict[str, str]]:
        system = (
            "You are a meticulous fact-checker for Wikipedia-quality content. "
            "Compare each numbered line from the candidate article against the reference article. "
            "Judge factual accuracy only. Ignore style, tone, or formatting differences. "
            "Cite issues precisely and conservatively. If uncertain, mark as 'uncertain'. "
            "Respond with strict JSON only, no additional commentary."
        )
        schema_hint = {
            "lines": [
                {
                    "line_number": 1,
                    "text": "Original line text here",
                    "status": "correct | partially_correct | incorrect | uncertain",
                    "issues": ["Describe specific factual inaccuracies or missing citations"],
                    "suggested_correction": "Proposed corrected version if applicable",
                    "confidence": 0.0
                }
            ],
            "summary": {
                "overall_assessment": "One paragraph summary of accuracy",
                "key_issues": ["Top issues observed"],
                "estimated_accuracy": 0.0
            }
        }
        user = (
            "Reference article:\n"
            "-----BEGIN REFERENCE-----\n"
            f"{reference_content}\n"
            "-----END REFERENCE-----\n\n"
            "Candidate article (numbered lines):\n"
            "-----BEGIN CANDIDATE-----\n"
            f"{numbered_generated}\n"
            "-----END CANDIDATE-----\n\n"
            "Return JSON only with the following structure:\n"
            f"{json.dumps(schema_hint, indent=2)}\n"
            "Requirements:\n"
            "- status must be one of: correct, partially_correct, incorrect, uncertain\n"
            "- confidence must be between 0.0 and 1.0\n"
            "- Include an entry for every line"
        )
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]

    def _parse_json_from_response(self, content: str) -> Dict[str, Any]:
        if not content:
            return {}
        # Try direct JSON
        try:
            return json.loads(content)
        except Exception:
            pass
        # Extract fenced code block ```json ... ```
        code_block = re.search(
            r"```json\s*(\{.*?\})\s*```", content, flags=re.S)
        if code_block:
            try:
                return json.loads(code_block.group(1))
            except Exception:
                pass
        # Extract first JSON object by braces
        brace_match = re.search(r"(\{.*\})", content, flags=re.S)
        if brace_match:
            chunk = brace_match.group(1)
            # Attempt to balance braces by truncating at last closing brace
            last = chunk.rfind("}")
            if last != -1:
                chunk = chunk[: last + 1]
            try:
                return json.loads(chunk)
            except Exception:
                pass
        return {}

    def _normalize_line_status(self, status: Optional[str]) -> str:
        if not isinstance(status, str):
            return "uncertain"
        s = status.strip().lower().replace("-", "_").replace(" ", "_")
        if s in {"correct", "partially_correct", "incorrect", "uncertain"}:
            return s
        # Map common variants
        if s in {"partial", "partially", "mixed", "partly_correct"}:
            return "partially_correct"
        if s in {"wrong", "false", "inaccurate"}:
            return "incorrect"
        if s in {"unknown", "unsure", "not_sure"}:
            return "uncertain"
        return "uncertain"

    def _coerce_float01(self, val: Any, default: float = 0.5) -> float:
        try:
            f = float(val)
            if f != f:  # NaN
                return default
            return max(0.0, min(1.0, f))
        except Exception:
            return default

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
        numbered, lines = self.prepare_article_for_evaluation(
            generated_article)
        messages = self._build_prompt(reference_content, numbered)

        raw_response_text = ""
        parsed: Dict[str, Any] = {}
        error: Optional[str] = None
        try:
            raw_response_text = self._call_openai(
                messages, temperature=temperature)
            parsed = self._parse_json_from_response(raw_response_text)
        except Exception as e:
            error = str(e)
            parsed = {}

        # Build normalized evaluation structure
        eval_lines: List[Dict[str, Any]] = []
        incoming_lines = []
        if isinstance(parsed.get("lines"), list):
            incoming_lines = parsed.get("lines")

        # Ensure an entry per line
        by_line: Dict[int, Dict[str, Any]] = {}
        # Ingest provided
        for entry in incoming_lines:
            if not isinstance(entry, dict):
                continue
            ln = entry.get("line_number")
            try:
                ln_int = int(ln)
            except Exception:
                continue
            if 1 <= ln_int <= len(lines):
                by_line[ln_int] = {
                    "line_number": ln_int,
                    "text": lines[ln_int - 1],
                    "status": self._normalize_line_status(entry.get("status")),
                    "issues": entry.get("issues") if isinstance(entry.get("issues"), list) else [],
                    "suggested_correction": entry.get("suggested_correction") if isinstance(entry.get("suggested_correction"), str) else "",
                    "confidence": self._coerce_float01(entry.get("confidence"), default=0.5),
                }

        # Fill missing
        for idx, text in enumerate(lines, start=1):
            if idx not in by_line:
                by_line[idx] = {
                    "line_number": idx,
                    "text": text,
                    "status": "uncertain",
                    "issues": [],
                    "suggested_correction": "",
                    "confidence": 0.5
                }

        eval_lines = [by_line[i] for i in sorted(by_line.keys())]

        summary = parsed.get("summary") if isinstance(
            parsed.get("summary"), dict) else {}
        normalized_summary = {
            "overall_assessment": summary.get("overall_assessment") if isinstance(summary.get("overall_assessment"), str) else "",
            "key_issues": summary.get("key_issues") if isinstance(summary.get("key_issues"), list) else [],
            "estimated_accuracy": self._coerce_float01(summary.get("estimated_accuracy"), default=None if eval_lines else 0.5)
        }

        result = {
            "lines": eval_lines,
            "summary": normalized_summary,
            "raw_response": raw_response_text,
        }
        if error:
            result["error"] = error
        return result

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        lines = evaluation_data.get("lines") if isinstance(
            evaluation_data, dict) else None
        vals: List[float] = []
        if isinstance(lines, list) and lines:
            for entry in lines:
                status = self._normalize_line_status(entry.get("status"))
                if status == "correct":
                    vals.append(1.0)
                elif status == "partially_correct":
                    vals.append(0.5)
                elif status == "incorrect":
                    vals.append(0.0)
                else:
                    vals.append(0.25)
            avg = sum(vals) / len(vals) if vals else 0.0
            score = 2.0 * avg - 1.0
            return max(-1.0, min(1.0, score))

        summary = evaluation_data.get("summary") if isinstance(
            evaluation_data, dict) else None
        if isinstance(summary, dict):
            acc = summary.get("estimated_accuracy")
            if isinstance(acc, (int, float)):
                score = 2.0 * float(acc) - 1.0
                return max(-1.0, min(1.0, score))

        return 0.0

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        lines = evaluation_data.get("lines") if isinstance(
            evaluation_data, dict) else None
        stats = {
            "total_lines": 0,
            "correct": 0,
            "partially_correct": 0,
            "incorrect": 0,
            "uncertain": 0,
            "avg_confidence": None,
            "accuracy_fraction": None,
            "score_-1_to_1": None
        }
        if not isinstance(lines, list) or not lines:
            stats["score_-1_to_1"] = self.calculate_accuracy_score(
                evaluation_data)
            return stats

        stats["total_lines"] = len(lines)
        confs: List[float] = []
        score_vals: List[float] = []

        for entry in lines:
            status = self._normalize_line_status(entry.get("status"))
            if status in stats:
                stats[status] += 1
            confs.append(self._coerce_float01(
                entry.get("confidence"), default=0.5))
            # For accuracy_fraction, treat correct=1, partial=0.5, incorrect=0, uncertain=0.25
            if status == "correct":
                score_vals.append(1.0)
            elif status == "partially_correct":
                score_vals.append(0.5)
            elif status == "incorrect":
                score_vals.append(0.0)
            else:
                score_vals.append(0.25)

        stats["avg_confidence"] = sum(confs) / len(confs) if confs else None
        stats["accuracy_fraction"] = sum(
            score_vals) / len(score_vals) if score_vals else None
        stats["score_-1_to_1"] = 2.0 * stats["accuracy_fraction"] - \
            1.0 if stats["accuracy_fraction"] is not None else None

        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        lines = evaluation_data.get("lines") if isinstance(
            evaluation_data, dict) else None
        if not isinstance(lines, list) or not lines:
            return pd.DataFrame(columns=["line_number", "text", "status", "confidence", "issues", "suggested_correction"])

        rows = []
        for e in lines:
            rows.append({
                "line_number": e.get("line_number"),
                "text": e.get("text"),
                "status": self._normalize_line_status(e.get("status")),
                "confidence": self._coerce_float01(e.get("confidence"), default=0.5),
                "issues": e.get("issues") if isinstance(e.get("issues"), list) else [],
                "suggested_correction": e.get("suggested_correction") if isinstance(e.get("suggested_correction"), str) else ""
            })
        return pd.DataFrame(rows)
