
import json
import os
from typing import Any, Dict, List, Optional, Tuple
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
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError(
                "OpenAI API key must be provided either directly or through the OPENAI_API_KEY environment variable")
        self.model = model
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
                return article.get('content')
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
                 for line in article_content.split('\n') if line.strip()]
        numbered_lines = [f"{i+1}. {line}" for i, line in enumerate(lines)]
        numbered_article = "\n".join(numbered_lines)
        return numbered_article, lines

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
        numbered_article, original_lines = self.prepare_article_for_evaluation(
            generated_article)

        prompt = f"""
        You are an expert fact-checker evaluating the accuracy of an AI-generated Wikipedia article against a reference article.
        Compare the AI-generated article to the reference article and evaluate each line for factual accuracy.

        Reference Article:
        {reference_content}

        AI-Generated Article (lines numbered for reference):
        {numbered_article}

        For each line in the AI-generated article, provide:
        1. The line number
        2. The original line text
        3. A boolean indicating if the line is factually accurate (True/False)
        4. A brief explanation of why the line is accurate or inaccurate

        Format your response as a JSON object with a 'lines' array containing objects for each line.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that evaluates the factual accuracy of text."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            response_format={"type": "json_object"}
        )

        evaluation_data = json.loads(response.choices[0].message.content)
        evaluation_data['original_lines'] = original_lines
        evaluation_data['reference_content'] = reference_content
        evaluation_data['generated_article'] = generated_article

        return evaluation_data

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        if not evaluation_data.get('lines'):
            return 0.0

        total_lines = len(evaluation_data['lines'])
        accurate_lines = sum(
            1 for line in evaluation_data['lines'] if line.get('is_accurate', False))

        if total_lines == 0:
            return 0.0

        accuracy_ratio = accurate_lines / total_lines
        normalized_score = (accuracy_ratio * 2) - 1  # Scale from -1 to 1

        return normalized_score

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        if not evaluation_data.get('lines'):
            return {
                'total_lines': 0,
                'accurate_lines': 0,
                'inaccurate_lines': 0,
                'accuracy_ratio': 0.0,
                'normalized_score': 0.0
            }

        total_lines = len(evaluation_data['lines'])
        accurate_lines = sum(
            1 for line in evaluation_data['lines'] if line.get('is_accurate', False))
        inaccurate_lines = total_lines - accurate_lines

        accuracy_ratio = accurate_lines / total_lines if total_lines > 0 else 0.0
        normalized_score = (accuracy_ratio * 2) - 1

        return {
            'total_lines': total_lines,
            'accurate_lines': accurate_lines,
            'inaccurate_lines': inaccurate_lines,
            'accuracy_ratio': accuracy_ratio,
            'normalized_score': normalized_score
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        if not evaluation_data.get('lines'):
            return pd.DataFrame()

        df = pd.DataFrame(evaluation_data['lines'])
        df['line_number'] = df['line_number'].astype(int)
        df['is_accurate'] = df['is_accurate'].astype(bool)

        # Add statistics to the DataFrame
        stats = self.calculate_accuracy_statistics(evaluation_data)
        for key, value in stats.items():
            df[key] = value

        return df
