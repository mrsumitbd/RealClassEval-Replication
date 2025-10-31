
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
        numbered_article, original_lines = self.prepare_article_for_evaluation(
            generated_article)

        prompt = f"""
        You are an expert fact-checker evaluating the accuracy of an AI-generated Wikipedia article against a reference article.
        The reference article is as follows:
        {reference_content}

        The AI-generated article is as follows (with lines numbered for reference):
        {numbered_article}

        For each line in the AI-generated article, determine if it is:
        1. Correct (matches the reference article)
        2. Incorrect (contradicts the reference article)
        3. Missing (information exists in reference but not in AI-generated article)
        4. Extra (information exists in AI-generated but not in reference)

        Return your evaluation as a JSON object with the following structure:
        {{
            "evaluation": [
                {{
                    "line_number": 1,
                    "content": "The content of line 1",
                    "accuracy": "correct|incorrect|missing|extra",
                    "explanation": "Brief explanation of why this line was classified as such"
                }},
                ...
            ],
            "summary": {{
                "correct": number,
                "incorrect": number,
                "missing": number,
                "extra": number,
                "total_lines": number
            }}
        }}
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
        return evaluation_data

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        summary = evaluation_data['summary']
        correct = summary['correct']
        incorrect = summary['incorrect']
        missing = summary['missing']
        extra = summary['extra']
        total = summary['total_lines']

        if total == 0:
            return 0.0

        # Calculate score components
        correct_score = correct / total
        incorrect_score = -incorrect / total
        missing_score = -missing / total
        extra_score = -extra / total

        # Combine scores with different weights
        total_score = (correct_score * 0.5) + (incorrect_score *
                                               0.3) + (missing_score * 0.1) + (extra_score * 0.1)

        # Normalize to -1 to 1 range
        normalized_score = max(-1.0, min(1.0, total_score * 2))

        return normalized_score

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        summary = evaluation_data['summary']
        total_lines = summary['total_lines']

        if total_lines == 0:
            return {
                'correct_percentage': 0.0,
                'incorrect_percentage': 0.0,
                'missing_percentage': 0.0,
                'extra_percentage': 0.0,
                'accuracy_score': 0.0
            }

        correct_percentage = (summary['correct'] / total_lines) * 100
        incorrect_percentage = (summary['incorrect'] / total_lines) * 100
        missing_percentage = (summary['missing'] / total_lines) * 100
        extra_percentage = (summary['extra'] / total_lines) * 100

        accuracy_score = self.calculate_accuracy_score(evaluation_data)

        return {
            'correct_percentage': correct_percentage,
            'incorrect_percentage': incorrect_percentage,
            'missing_percentage': missing_percentage,
            'extra_percentage': extra_percentage,
            'accuracy_score': accuracy_score
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        evaluation_lines = evaluation_data['evaluation']
        df = pd.DataFrame(evaluation_lines)

        # Add original line content
        df['original_line'] = evaluation_data['original_lines']

        # Add summary statistics
        summary = evaluation_data['summary']
        stats = self.calculate_accuracy_statistics(evaluation_data)

        # Create a summary row
        summary_row = {
            'line_number': 'Summary',
            'content': '',
            'accuracy': '',
            'explanation': '',
            'original_line': '',
            'correct': summary['correct'],
            'incorrect': summary['incorrect'],
            'missing': summary['missing'],
            'extra': summary['extra'],
            'total_lines': summary['total_lines'],
            'correct_percentage': stats['correct_percentage'],
            'incorrect_percentage': stats['incorrect_percentage'],
            'missing_percentage': stats['missing_percentage'],
            'extra_percentage': stats['extra_percentage'],
            'accuracy_score': stats['accuracy_score']
        }

        # Convert to DataFrame and append summary row
        summary_df = pd.DataFrame([summary_row])
        result_df = pd.concat([df, summary_df], ignore_index=True)

        return result_df
