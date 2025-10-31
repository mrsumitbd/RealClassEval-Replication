
import os
from typing import Optional, Dict, Any, Tuple, List
import pandas as pd
import openai
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
        self.api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        if self.api_key:
            openai.api_key = self.api_key

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
        lines = [line.strip()
                 for line in article_content.split('\n') if line.strip()]
        numbered_lines = [f"{i+1}. {line}" for i, line in enumerate(lines)]
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
        numbered_article, original_lines = self.prepare_article_for_evaluation(
            generated_article)
        prompt = f"""
        Evaluate the factual accuracy of the following AI-generated Wikipedia article against the reference article.
        For each numbered line in the generated article, provide:
        - 'accurate' if the information is factually correct
        - 'inaccurate' if the information is factually incorrect
        - 'unverifiable' if the information cannot be verified from the reference
        - 'not_found' if the information is not present in the reference

        Reference Article:
        {reference_content}

        Generated Article:
        {numbered_article}

        Provide your evaluation in JSON format with line numbers as keys and the evaluation result as values.
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a fact-checking assistant that evaluates Wikipedia articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            response_format={"type": "json_object"}
        )

        evaluation = json.loads(response.choices[0].message.content)
        return {
            'evaluation': evaluation,
            'original_lines': original_lines,
            'reference_content': reference_content,
            'generated_article': generated_article
        }

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        evaluation = evaluation_data.get('evaluation', {})
        scores = {
            'accurate': 1,
            'inaccurate': -1,
            'unverifiable': 0,
            'not_found': 0
        }
        total = 0
        count = 0
        for line_result in evaluation.values():
            if isinstance(line_result, dict):
                result = line_result.get('verdict', 'unverifiable')
            else:
                result = line_result
            total += scores.get(result.lower(), 0)
            count += 1
        return total / max(count, 1)

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        evaluation = evaluation_data.get('evaluation', {})
        stats = {
            'accurate': 0,
            'inaccurate': 0,
            'unverifiable': 0,
            'not_found': 0,
            'total_lines': 0
        }
        for line_result in evaluation.values():
            if isinstance(line_result, dict):
                result = line_result.get('verdict', 'unverifiable')
            else:
                result = line_result
            stats[result.lower()] += 1
            stats['total_lines'] += 1
        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        evaluation = evaluation_data.get('evaluation', {})
        original_lines = evaluation_data.get('original_lines', [])
        rows = []
        for line_num, result in evaluation.items():
            if isinstance(result, dict):
                verdict = result.get('verdict', 'unverifiable')
                explanation = result.get('explanation', '')
            else:
                verdict = result
                explanation = ''
            try:
                line_idx = int(line_num.split('.')[0]) - 1
                line_text = original_lines[line_idx] if line_idx < len(
                    original_lines) else ''
            except:
                line_text = ''
            rows.append({
                'line_number': line_num,
                'line_text': line_text,
                'verdict': verdict,
                'explanation': explanation
            })
        return pd.DataFrame(rows)
