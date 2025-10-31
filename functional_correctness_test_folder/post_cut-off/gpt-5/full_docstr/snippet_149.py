from typing import Optional, Dict, List, Tuple, Any
import os
import json
import re

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
        self.model = model
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        self._client_mode = None  # 'new' or 'legacy'
        if self.api_key:
            # Try new OpenAI client first
            try:
                import openai as openai_new  # new SDK (>=1.0)
                # New SDK prefers: from openai import OpenAI; client = OpenAI()
                from openai import OpenAI  # type: ignore
                self.client = OpenAI(api_key=self.api_key)
                self._client_mode = 'new'
            except Exception:
                # Fallback to legacy openai module
                try:
                    import openai as openai_legacy  # type: ignore
                    openai_legacy.api_key = self.api_key
                    self.client = openai_legacy
                    self._client_mode = 'legacy'
                except Exception:
                    self.client = None
                    self._client_mode = None

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

        def _extract_text(obj: Any) -> Optional[str]:
            if obj is None:
                return None
            # Try common fields that may contain article text
            for key in ['text', 'extract', 'content', 'body', 'article', 'plain_text']:
                if isinstance(obj, dict) and key in obj and isinstance(obj[key], str):
                    return obj[key].strip() or None
            # If object is directly a string
            if isinstance(obj, str):
                s = obj.strip()
                return s or None
            return None

        # Direct mapping by title
        if isinstance(json_data, dict) and title in json_data:
            txt = _extract_text(json_data[title])
            if txt:
                return txt

        # Case-insensitive search among top-level dict keys
        if isinstance(json_data, dict):
            for k, v in json_data.items():
                if isinstance(k, str) and k.lower() == title.lower():
                    txt = _extract_text(v)
                    if txt:
                        return txt

        # Nested common structures
        # e.g., {"articles": [{"title": "...", "text": "..."}]}
        for key in ['articles', 'pages', 'entries', 'items', 'data']:
            container = json_data.get(key) if isinstance(
                json_data, dict) else None
            if isinstance(container, list):
                for item in container:
                    if isinstance(item, dict):
                        t = item.get('title') or item.get(
                            'name') or item.get('page') or item.get('id')
                        if isinstance(t, str) and t.lower() == title.lower():
                            txt = _extract_text(item)
                            if txt:
                                return txt

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
        lines = [ln.rstrip() for ln in str(article_content).splitlines()]
        # Preserve blank lines but mark them as empty for clarity
        numbered_lines = []
        for i, ln in enumerate(lines, start=1):
            content = ln if ln.strip() != "" else ""
            numbered_lines.append(f"{i}. {content}")
        return "\n".join(numbered_lines), lines

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
        numbered_text, original_lines = self.prepare_article_for_evaluation(
            generated_article)

        system_prompt = (
            "You are a meticulous fact-checking assistant. Evaluate an AI-generated Wikipedia article "
            "against the provided reference article. For each line, determine if it is factually Correct, "
            "Incorrect, or Unsure based solely on the reference. If Incorrect, provide a minimal correction. "
            "Return STRICT JSON with the following schema:\n"
            "{\n"
            '  "per_line": [\n'
            '     {\n'
            '       "line_number": int,\n'
            '       "text": string,\n'
            '       "verdict": "correct" | "incorrect" | "unsure",\n'
            '       "explanation": string,\n'
            '       "corrections": [string]\n'
            "     }, ...\n"
            "  ],\n"
            '  "notes": string\n'
            "}\n"
            "Do not include any additional text outside of the JSON."
        )

        user_prompt = (
            "Reference Article:\n"
            "------------------\n"
            f"{reference_content}\n\n"
            "AI-Generated Article (numbered lines):\n"
            "--------------------------------------\n"
            f"{numbered_text}\n\n"
            "Evaluate every line from 1 to "
            f"{len(original_lines)}."
        )

        result: Dict[str, Any] = {
            "per_line": [],
            "notes": "",
            "model": self.model,
            "used_llm": bool(self.client),
            "raw_response": None,
        }

        content = None
        if self.client:
            content = self._call_openai(
                system_prompt, user_prompt, temperature)

        if content is None:
            # Fallback heuristic if API not available or failed: mark lines as "unsure"
            per_line = []
            for i, text in enumerate(original_lines, start=1):
                per_line.append({
                    "line_number": i,
                    "text": text,
                    "verdict": "unsure" if text.strip() else "unsure",
                    "explanation": "No LLM evaluation available; defaulting to unsure.",
                    "corrections": []
                })
            result["per_line"] = per_line
            result["notes"] = "LLM evaluation unavailable or failed; all lines marked as unsure."
            return result

        result["raw_response"] = content

        parsed = self._extract_json(content)
        if not parsed:
            # If extraction fails, still return a structured fallback
            per_line = []
            for i, text in enumerate(original_lines, start=1):
                per_line.append({
                    "line_number": i,
                    "text": text,
                    "verdict": "unsure",
                    "explanation": "Could not parse model JSON output.",
                    "corrections": []
                })
            result["per_line"] = per_line
            result["notes"] = "Could not parse model JSON output."
            return result

        # Normalize parsed content
        per_line_out = []
        per_line = parsed.get("per_line", [])
        for entry in per_line:
            ln = entry.get("line_number")
            tx = entry.get("text", "")
            verdict = str(entry.get("verdict", "")).strip().lower()
            if verdict not in ("correct", "incorrect", "unsure"):
                verdict = "unsure"
            explanation = entry.get("explanation", "")
            corrections = entry.get("corrections", [])
            if not isinstance(corrections, list):
                corrections = [str(corrections)]
            # Ensure line numbers make sense
            if not isinstance(ln, int) or ln < 1 or ln > len(original_lines):
                # Attempt to map by index if possible
                ln = min(len(per_line_out) + 1, len(original_lines))
            # Ensure text is original line if not provided or mismatched
            if not tx:
                tx = original_lines[ln - 1]
            per_line_out.append({
                "line_number": ln,
                "text": tx,
                "verdict": verdict,
                "explanation": explanation,
                "corrections": [str(c) for c in corrections]
            })

        # Ensure we have entries for all lines
        have = {e["line_number"]
                for e in per_line_out if isinstance(e.get("line_number"), int)}
        for i in range(1, len(original_lines) + 1):
            if i not in have:
                per_line_out.append({
                    "line_number": i,
                    "text": original_lines[i - 1],
                    "verdict": "unsure",
                    "explanation": "Line missing from model output; marked as unsure.",
                    "corrections": []
                })

        # Sort by line_number
        per_line_out.sort(key=lambda x: x.get("line_number", 0))

        result["per_line"] = per_line_out
        result["notes"] = parsed.get("notes", "")
        return result

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        per_line = evaluation_data.get("per_line", []) if isinstance(
            evaluation_data, dict) else []
        correct = sum(1 for e in per_line if str(
            e.get("verdict", "")).lower() == "correct")
        incorrect = sum(1 for e in per_line if str(
            e.get("verdict", "")).lower() == "incorrect")
        evaluated = correct + incorrect
        if evaluated == 0:
            return 0.0
        score = (correct - incorrect) / float(evaluated)
        # Clamp just in case
        return max(-1.0, min(1.0, score))

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        per_line = evaluation_data.get("per_line", []) if isinstance(
            evaluation_data, dict) else []
        total_lines = len(per_line)
        correct = sum(1 for e in per_line if str(
            e.get("verdict", "")).lower() == "correct")
        incorrect = sum(1 for e in per_line if str(
            e.get("verdict", "")).lower() == "incorrect")
        unsure = sum(1 for e in per_line if str(
            e.get("verdict", "")).lower() == "unsure")
        evaluated = correct + incorrect
        accuracy = (correct / evaluated) if evaluated > 0 else None
        net_score = self.calculate_accuracy_score(evaluation_data)

        return {
            "total_lines": total_lines,
            "evaluated_lines": evaluated,
            "correct": correct,
            "incorrect": incorrect,
            "unsure": unsure,
            "accuracy": accuracy,
            "net_score": net_score,
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        per_line = evaluation_data.get("per_line", []) if isinstance(
            evaluation_data, dict) else []
        rows = []
        for e in per_line:
            rows.append({
                "line_number": e.get("line_number"),
                "text": e.get("text"),
                "verdict": e.get("verdict"),
                "explanation": e.get("explanation"),
                "corrections": e.get("corrections"),
            })
        df = pd.DataFrame(
            rows, columns=["line_number", "text", "verdict", "explanation", "corrections"])
        return df

    def _call_openai(self, system_prompt: str, user_prompt: str, temperature: float) -> Optional[str]:
        try:
            if self._client_mode == 'new':
                # New SDK
                resp = self.client.chat.completions.create(
                    model=self.model,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"},
                )
                content = resp.choices[0].message.content if resp and resp.choices else None
                return content
            elif self._client_mode == 'legacy':
                # Legacy SDK
                resp = self.client.ChatCompletion.create(
                    model=self.model,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                content = resp["choices"][0]["message"]["content"] if resp and resp.get(
                    "choices") else None
                return content
            else:
                return None
        except Exception:
            return None

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        # Try direct JSON parse
        try:
            return json.loads(text)
        except Exception:
            pass

        # Try code block fenced JSON ```json ... ```
        codeblock = re.search(r"```json\s*(.*?)\s*```",
                              text, flags=re.DOTALL | re.IGNORECASE)
        if codeblock:
            snippet = codeblock.group(1)
            try:
                return json.loads(snippet)
            except Exception:
                pass

        # Try to find a JSON object by balancing braces
        start_idxs = [m.start() for m in re.finditer(r"\{", text)]
        for si in start_idxs:
            depth = 0
            for ei in range(si, len(text)):
                if text[ei] == "{":
                    depth += 1
                elif text[ei] == "}":
                    depth -= 1
                    if depth == 0:
                        candidate = text[si:ei+1]
                        try:
                            return json.loads(candidate)
                        except Exception:
                            break
        return None
