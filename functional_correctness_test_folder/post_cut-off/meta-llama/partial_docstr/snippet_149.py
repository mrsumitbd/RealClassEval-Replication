
import os
from typing import Optional, Dict, Tuple, List, Any
import pandas as pd
from openai import OpenAI


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
            raise ValueError("OpenAI API key is required")
        self.client = OpenAI(api_key=self.openai_api_key)

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
        lines = article_content.strip().split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return '\n'.join(cleaned_lines), cleaned_lines

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
        reference_text, reference_lines = self.prepare_article_for_evaluation(
            reference_content)
        generated_text, generated_lines = self.prepare_article_for_evaluation(
            generated_article)

        prompt = f"""
        Compare the factual accuracy of the following two articles line by line.
        Reference Article:
        {reference_text}
        
        Generated Article:
        {generated_text}
        
        For each line in the generated article, determine if it is factually accurate compared to the reference article.
        Return a JSON object with the following structure:
        {{
            "line_evaluations": [
                {{
                    "line": "<generated line>",
                    "accuracy": "<accurate/inaccurate/unknown>",
                    "reference_line": "<corresponding reference line if available>",
                    "explanation": "<brief explanation>"
                }},
                ...
            ],
            "overall_accuracy": "<overall assessment>"
        }}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to evaluate the factual accuracy of articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        try:
            evaluation_data = response.choices[0].message.content
            import json
            evaluation_data = json.loads(evaluation_data)
        except Exception as e:
            print(f"Error parsing evaluation response: {e}")
            evaluation_data = {"line_evaluations": [],
                               "overall_accuracy": "unknown"}

        return evaluation_data

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        line_evaluations = evaluation_data.get('line_evaluations', [])
        accurate_count = sum(
            1 for eval in line_evaluations if eval.get('accuracy') == 'accurate')
        total_count = len(line_evaluations)
        if total_count == 0:
            return 0
        accuracy = accurate_count / total_count
        return 2 * accuracy - 1  # Normalize to [-1, 1] range

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        line_evaluations = evaluation_data.get('line_evaluations', [])
        total_lines = len(line_evaluations)
        accurate_count = sum(
            1 for eval in line_evaluations if eval.get('accuracy') == 'accurate')
        inaccurate_count = sum(
            1 for eval in line_evaluations if eval.get('accuracy') == 'inaccurate')
        unknown_count = total_lines - accurate_count - inaccurate_count

        return {
            'total_lines': total_lines,
            'accurate_lines': accurate_count,
            'inaccurate_lines': inaccurate_count,
            'unknown_lines': unknown_count,
            'accuracy_percentage': (accurate_count / total_lines * 100) if total_lines > 0 else 0
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        line_evaluations = evaluation_data.get('line_evaluations', [])
        df = pd.DataFrame(line_evaluations)
        return df
