
import os
import json
from typing import Dict, Optional, Tuple, List, Any
import pandas as pd
import openai


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
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError(
                "OpenAI API key must be provided or set as OPENAI_API_KEY environment variable")
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
        for article in json_data.get('articles', []):
            if article.get('title') == title:
                return article.get('text')
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
        lines = article_content.split('\n')
        numbered_lines = [f"{i+1}. {line}" for i,
                          line in enumerate(lines) if line.strip()]
        return '\n'.join(numbered_lines), lines

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
        prompt = f"""
        Reference Article:
        {reference_content}

        Generated Article:
        {generated_article}

        Evaluate each line of the generated article for factual accuracy against the reference article. 
        For each line, provide:
        - 'accurate': True if the information is factually correct, False otherwise
        - 'explanation': A brief explanation of the inaccuracy if applicable
        - 'severity': Low/Medium/High for inaccuracies (None if accurate)
        Return the evaluation as a JSON object with line numbers as keys.
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a fact-checking assistant that evaluates Wikipedia articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        evaluation = json.loads(response.choices[0].message['content'])
        return evaluation

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        total_lines = len(evaluation_data)
        if total_lines == 0:
            return 0.0

        accurate_lines = sum(
            1 for line in evaluation_data.values() if line.get('accurate', False))
        return (2 * (accurate_lines / total_lines)) - 1  # Scale to [-1, 1]

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        total_lines = len(evaluation_data)
        accurate_lines = sum(
            1 for line in evaluation_data.values() if line.get('accurate', False))
        severity_counts = {
            'low': sum(1 for line in evaluation_data.values() if line.get('severity') == 'Low'),
            'medium': sum(1 for line in evaluation_data.values() if line.get('severity') == 'Medium'),
            'high': sum(1 for line in evaluation_data.values() if line.get('severity') == 'High')
        }

        return {
            'total_lines': total_lines,
            'accurate_lines': accurate_lines,
            'inaccurate_lines': total_lines - accurate_lines,
            'accuracy_percentage': (accurate_lines / total_lines) * 100 if total_lines > 0 else 0,
            'severity_counts': severity_counts
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        rows = []
        for line_num, data in evaluation_data.items():
            row = {
                'line_number': line_num,
                'accurate': data.get('accurate', False),
                'explanation': data.get('explanation', ''),
                'severity': data.get('severity', None)
            }
            rows.append(row)

        return pd.DataFrame(rows)
