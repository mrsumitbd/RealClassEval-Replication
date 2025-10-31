
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
        # Assume json_data is a dict mapping titles to article dicts with a 'text' field
        article = json_data.get(title)
        if article is None:
            return None
        # If article is a dict with 'text', return that; otherwise assume it's the text itself
        if isinstance(article, dict):
            return article.get("text")
        return article

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
                n=1,
                stop=None,
            )
            content = response.choices[0].message.content.strip()
            # Try to parse JSON; if fails, return raw content
            try:
                eval_data = json.loads(content)
            except json.JSONDecodeError:
                eval_data = {"error": "Failed to parse JSON",
                             "raw_response": content}
        except Exception as e:
            eval_data = {"error": str(e)}

        # Attach original lines for reference
        if isinstance(eval_data, list):
            for item in eval_data:
                line_num = int(item.get("line_number", 0))
                if 1 <= line_num <= len(original_lines):
                    item["original_text"] = original_lines[line_num - 1]
        return eval_data

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        """
        Calculate a normalized accuracy score from evaluation data.

        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy

        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        """
        if not isinstance(evaluation_data, list) or not evaluation_data:
            return 0.0

        score_map = {"accurate": 1.0,
                     "partially accurate": 0.5, "inaccurate": 0.0}
        scores = []
        for item in evaluation_data:
            acc = item.get("accuracy", "").lower()
            scores.append(score_map.get(acc, 0.0))
        avg = sum(scores) / len(scores)
        # Map 0.0 -> -1, 0.5 -> 0, 1.0 -> 1
        return (avg - 0.5) * 2

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        """
        Calculate statistics from the evaluation data.

        Args:
            evaluation_data: The line-by-line evaluation dictionary

        Returns:
            Dictionary with accuracy statistics
        """
        if not isinstance(evaluation_data, list) or not evaluation_data:
            return {"total_lines": 0, "accurate": 0, "partial": 0, "inaccurate": 0}

        stats = {"total_lines": len(evaluation_data),
                 "accurate": 0, "partial": 0, "inaccurate": 0}
        for item in evaluation_data:
            acc = item.get("accuracy", "").lower()
            if acc == "accurate":
                stats["accurate"] += 1
            elif acc == "partially accurate":
                stats["partial"] += 1
            elif acc == "inaccurate":
                stats["inaccurate"] += 1
        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        """
        Convert evaluation data to a pandas DataFrame for easier analysis.

        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy

        Returns:
            DataFrame with evaluation results
        """
        if not isinstance(evaluation_data, list):
            return pd.DataFrame()
        df = pd.DataFrame(evaluation_data)
        # Ensure consistent column order
        cols = ["line_number", "text",
                "original_text", "accuracy", "explanation"]
        df = df.reindex(columns=cols)
        return df
