
import os
import json
from typing import Any, Dict, List, Optional, Tuple

import openai
import pandas as pd


class ArticleEvaluator:
    """
    A class to evaluate the factual accuracy of AI-generated Wikipedia articles
    against reference articles using OpenAI models.
    """

    def __init__(self, openai_api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialize the ArticleEvaluator with API credentials and model settings.

        Args:
            openai_api_key: API key for OpenAI (falls back to OPENAI_API_KEY env var)
            model: The OpenAI model to use for evaluation (default: gpt-4o)
        """
        self.model = model
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key must be provided or set in OPENAI_API_KEY env var")
        openai.api_key = self.api_key

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        """
        Retrieve reference article text from the JSON data.

        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve

        Returns:
            The plain text content of the reference article, or None if not found
        """
        # Assume json_data is a mapping from title to article dict containing 'text'
        article = json_data.get(title)
        if article is None:
            return None
        # If article is a dict with 'text' key
        if isinstance(article, dict):
            return article.get("text")
        # If article is a string
        if isinstance(article, str):
            return article
        return None

    def prepare_article_for_evaluation(
        self, article_content: str
    ) -> Tuple[str, List[str]]:
        """
        Prepare an AI-generated article for evaluation by numbering its lines.

        Args:
            article_content: The content of the AI-generated article

        Returns:
            A tuple containing:
            - Numbered article text suitable for the prompt
            - List of the original lines for further processing
        """
        lines = article_content.splitlines()
        numbered_lines = [f"{idx + 1}. {line}" for idx,
                          line in enumerate(lines)]
        numbered_text = "\n".join(numbered_lines)
        return numbered_text, lines

    def evaluate_article_accuracy(
        self,
        reference_content: str,
        generated_article: str,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        """
        Evaluate the factual accuracy of an AI-generated article against a reference.

        Args:
            reference_content: The text of the reference Wikipedia article
            generated_article: The text of the AI-generated article
            temperature: The sampling temperature for the OpenAI API call

        Returns:
            Dictionary containing the evaluation results
        """
        numbered_article, original_lines = self.prepare_article_for_evaluation(
            generated_article
        )

        prompt = (
            "You are a Wikipedia fact-checker. Compare the following reference article "
            "with the generated article. For each line in the generated article, indicate "
            "whether it is accurate, partially accurate, or inaccurate. Provide a brief "
            "explanation for each line. Return the result as a JSON array where each "
            "element has the keys: line_number, text, accuracy, explanation.\n\n"
            f"Reference article:\n{reference_content}\n\n"
            f"Generated article:\n{numbered_article}\n\n"
            "Answer in JSON format only."
        )

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1500,
            )
            content = response.choices[0].message.content.strip()
            # Try to parse JSON
            try:
                eval_data = json.loads(content)
            except json.JSONDecodeError:
                # If the response is not valid JSON, attempt to extract JSON substring
                start = content.find("{")
                end = content.rfind("}")
                if start != -1 and end != -1:
                    eval_data = json.loads(content[start: end + 1])
                else:
                    raise ValueError(
                        "Unable to parse evaluation response as JSON")
        except Exception as exc:
            raise RuntimeError(f"OpenAI API call failed: {exc}") from exc

        # Ensure eval_data is a list of dicts
        if not isinstance(eval_data, list):
            raise ValueError("Evaluation response JSON is not a list")

        # Attach line numbers and original text if missing
        for idx, item in enumerate(eval_data):
            if "line_number" not in item:
                item["line_number"] = idx + 1
            if "text" not in item and idx < len(original_lines):
                item["text"] = original_lines[idx]
            if "accuracy" not in item:
                item["accuracy"] = "unknown"
            if "explanation" not in item:
                item["explanation"] = ""

        return {"lines": eval_data}

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        """
        Calculate a normalized accuracy score from evaluation data.

        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy

        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        """
        lines = evaluation_data.get("lines", [])
        if not lines:
            return 0.0

        score_map = {"accurate": 1.0,
                     "partially accurate": 0.5, "inaccurate": 0.0}
        scores = []
        for line in lines:
            acc = line.get("accuracy", "").lower()
            scores.append(score_map.get(acc, 0.0))

        avg = sum(scores) / len(scores)
        # Map 0.0 -> -1, 1.0 -> 1
        return (avg * 2) - 1

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        """
        Calculate statistics from the evaluation data.

        Args:
            evaluation_data: The line-by-line evaluation dictionary

        Returns:
            Dictionary with accuracy statistics
        """
        lines = evaluation_data.get("lines", [])
        total = len(lines)
        if total == 0:
            return {"total_lines": 0, "accurate": 0, "partial": 0, "inaccurate": 0}

        counts = {"accurate": 0, "partially accurate": 0, "inaccurate": 0}
        for line in lines:
            acc = line.get("accuracy", "").lower()
            if acc in counts:
                counts[acc] += 1

        stats = {
            "total_lines": total,
            "accurate": counts["accurate"],
            "partial": counts["partially accurate"],
            "inaccurate": counts["inaccurate"],
            "accuracy_rate": counts["accurate"] / total,
            "partial_rate": counts["partially accurate"] / total,
            "inaccuracy_rate": counts["inaccurate"] / total,
        }
        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        """
        Convert evaluation data to a pandas DataFrame for easier analysis.

        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy

        Returns:
            DataFrame with evaluation results
        """
        lines = evaluation_data.get("lines", [])
        df = pd.DataFrame(lines)
        # Ensure consistent column order
        expected_cols = ["line_number", "text", "accuracy", "explanation"]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None
        df = df[expected_cols]
        return df
