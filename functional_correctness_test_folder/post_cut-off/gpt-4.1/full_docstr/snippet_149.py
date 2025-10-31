
import os
from typing import Optional, Dict, Any, Tuple, List
import openai
import pandas as pd
import re
import json


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
        if openai_api_key is None:
            openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.openai_api_key = openai_api_key
        self.model = model
        openai.api_key = self.openai_api_key

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        '''
        Retrieve reference article text from the JSON data.
        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve
        Returns:
            The plain text content of the reference article, or None if not found
        '''
        if title in json_data:
            article = json_data[title]
            if isinstance(article, dict) and 'text' in article:
                return article['text']
            elif isinstance(article, str):
                return article
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
        lines = [line.strip()
                            for line in article_content.strip().split('\n') if line.strip()]
        numbered_lines = [f"{i+1}. {line}" for i, line in enumerate(lines)]
        numbered_text = "\n".join(numbered_lines)
        return numbered_text, lines

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
        numbered_text, lines = self.prepare_article_for_evaluation(
            generated_article)
        prompt = (
            "You are a Wikipedia expert. Given the following reference article and an AI-generated article, "
            "evaluate the factual accuracy of each line in the AI-generated article. "
            "For each line, respond with a JSON list of objects, one per line, with the following fields:\n"
            "- line_number (int)\n"
            "- text (str)\n"
            "- accurate (bool): Is the statement factually accurate compared to the reference?\n"
            "- error_type (str): 'factual', 'minor', 'missing', 'hallucination', or 'none'\n"
            "- explanation (str): Brief explanation if not accurate, else empty string\n\n"
            "Reference Article:\n"
            f"{reference_content}\n\n"
            "AI-Generated Article (numbered lines):\n"
            f"{numbered_text}\n\n"
            "Respond ONLY with the JSON list."
        )
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for Wikipedia factual accuracy evaluation."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=2048,
        )
        content = response.choices[0].message.content.strip()
        # Extract JSON from the response
        try:
            # Try to parse directly
            if content.startswith('
