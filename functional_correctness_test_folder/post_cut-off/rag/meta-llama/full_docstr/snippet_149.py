
import os
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import openai


class ArticleEvaluator:
    """
    A class to evaluate the factual accuracy of AI-generated Wikipedia articles
    against reference articles using OpenAI models.
    """

    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4o'):
        """
        Initialize the ArticleEvaluator with API credentials and model settings.
        Args:
            openai_api_key: API key for OpenAI (falls back to OPENAI_API_KEY env var)
            model: The OpenAI model to use for evaluation (default: gpt-4o)
        """
        self.openai_api_key = openai_api_key or os.environ.get(
            'OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError(
                "OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")

        openai.api_key = self.openai_api_key
        self.model = model

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        """
        Retrieve reference article text from the JSON data.
        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve
        Returns:
            The plain text content of the reference article, or None if not found
        """
        for article in json_data.get('articles', []):
            if article.get('title') == title:
                return article.get('text')
        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        """
        Prepare an AI-generated article for evaluation by numbering its lines.
        Args:
            article_content: The content of the AI-generated article
        Returns:
            A tuple containing:
            - Numbered article text suitable for the prompt
            - List of the original lines for further processing
        """
        lines = article_content.split('\n')
        numbered_lines = [f"{i+1}. {line}" for i, line in enumerate(lines)]
        numbered_article = '\n'.join(numbered_lines)
        return numbered_article, lines

    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float = 0.2) -> Dict[str, Any]:
        """
        Evaluate the factual accuracy of an AI-generated article against a reference.
        Args:
            reference_content: The text of the reference Wikipedia article
            generated_article: The text of the AI-generated article
            temperature: The sampling temperature for the OpenAI API call
        Returns:
            Dictionary containing the evaluation results
        """
        prompt = f"""Evaluate the factual accuracy of the following AI-generated Wikipedia article against the reference article. 
        Reference article: {reference_content}
        AI-generated article (numbered lines): {generated_article}
        
        For each line in the AI-generated article, provide:
        1. The line number
        2. The original statement
        3. 'True' if the statement is factually correct according to the reference, 'False' otherwise
        4. A brief explanation for your judgment
        
        Format your response as a JSON object with the line number as keys and objects containing the evaluation results as values.
        """

        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            response_format={"type": "json_object"}
        )

        try:
            evaluation_data = response.choices[0].message.content
            # Using eval here for simplicity; consider using json.loads for safer parsing
            return eval(evaluation_data)
        except Exception as e:
            print(f"Error parsing evaluation response: {e}")
            return {}

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        """
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        """
        total_lines = len(evaluation_data)
        if total_lines == 0:
            return 0

        correct_count = sum(1 for eval_result in evaluation_data.values(
        ) if eval_result.get('accuracy') == 'True')
        accuracy = correct_count / total_lines
        # Normalize to -1 to 1 range
        normalized_score = 2 * accuracy - 1
        return normalized_score

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        """
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        """
        total_lines = len(evaluation_data)
        correct_count = sum(1 for eval_result in evaluation_data.values(
        ) if eval_result.get('accuracy') == 'True')
        incorrect_count = total_lines - correct_count

        stats = {
            'total_lines': total_lines,
            'correct_lines': correct_count,
            'incorrect_lines': incorrect_count,
            'accuracy': correct_count / total_lines if total_lines > 0 else 0
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
        data = []
        for line_num, eval_result in evaluation_data.items():
            data.append({
                'line_number': line_num,
                'statement': eval_result.get('statement'),
                'accuracy': eval_result.get('accuracy'),
                'explanation': eval_result.get('explanation')
            })
        return pd.DataFrame(data)
