
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

    # ------------------------------------------------------------------
    # Reference article retrieval
    # ------------------------------------------------------------------
    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        """
        Retrieve reference article text from the JSON data.

        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve

        Returns:
            The plain text content of the reference article, or None if not found
        """
        # Case 1: json_data is a dict mapping titles to content
        if isinstance(json_data, dict):
            if title in json_data:
                return json_data[title]
            # Some datasets use nested structure: {"title": ..., "content": ...}
            for key, value in json_data.items():
                if isinstance(value, dict):
                    if value.get("title") == title:
                        return value.get("content")
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict) and item.get("title") == title:
                            return item.get("content")

        # Case 2: json_data is a list of article dicts
        if isinstance(json_data, list):
            for article in json_data:
                if isinstance(article, dict):
                    if article.get("title") == title:
                        return article.get("content")

        return None

    # ------------------------------------------------------------------
    # Article preparation
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------
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
            "You are a Wikipedia fact-checker. "
            "Compare the following AI-generated article with the reference Wikipedia article. "
            "For each numbered line in the AI-generated article, determine whether it is factually correct "
            "according to the reference. Provide a confidence score between 0 and 1. "
            "If a line is incorrect, provide the correct information from the reference. "
            "Return the result as a JSON array of objects with the following keys:\n"
            "  - line_number (int)\n"
            "  - line_text (string)\n"
            "  - is_correct (bool)\n"
            "  - confidence (float)\n"
            "  - correction (string, optional)\n\n"
            f"Reference article:\n{reference_content}\n\n"
            f"AI-generated article:\n{numbered_article}\n\n"
            "Answer in JSON format only."
        )

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
            )
            raw_text = response.choices[0].message.content.strip()
            # Ensure JSON is valid
            if raw_text.startswith("
