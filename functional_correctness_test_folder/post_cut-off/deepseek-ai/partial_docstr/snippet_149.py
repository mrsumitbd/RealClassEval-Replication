
import os
from typing import Optional, Dict, Any, List, Tuple
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
        self.api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key is None:
            raise ValueError(
                "OpenAI API key must be provided or set as environment variable OPENAI_API_KEY")
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
        Prepare an article for evaluation by splitting into sections.
        Args:
            article_content: The text of the article to prepare
        Returns:
            A tuple of (cleaned_text, sections)
        '''
        sections = article_content.split('\n\n')
        cleaned_text = '\n\n'.join(sections)
        return cleaned_text, sections

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
        Compare the following AI-generated Wikipedia article with the reference article and evaluate its factual accuracy.
        For each factual claim in the generated article, determine if it is:
        - Correct (matches reference)
        - Incorrect (contradicts reference)
        - Unverifiable (not mentioned in reference)
        - Partially correct (some elements match but others don't)

        Reference Article:
        {reference_content}

        Generated Article:
        {generated_article}

        Provide your evaluation as a JSON object with the following structure:
        {
            "overall_accuracy": "summary evaluation",
            "line_by_line": [
                {
                    "text": "excerpt from generated article",
                    "verdict": "Correct/Incorrect/Unverifiable/Partially correct",
                    "explanation": "detailed explanation"
                },
                ...
            ]
        }
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
        return eval(response.choices[0].message.content)

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        line_by_line = evaluation_data.get('line_by_line', [])
        if not line_by_line:
            return 0.0

        scores = []
        for item in line_by_line:
            verdict = item.get('verdict', '').lower()
            if verdict == 'correct':
                scores.append(1.0)
            elif verdict == 'partially correct':
                scores.append(0.5)
            elif verdict == 'unverifiable':
                scores.append(0.0)
            elif verdict == 'incorrect':
                scores.append(-1.0)

        return sum(scores) / len(scores) if scores else 0.0

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        line_by_line = evaluation_data.get('line_by_line', [])
        if not line_by_line:
            return {
                'total_claims': 0,
                'correct': 0,
                'incorrect': 0,
                'unverifiable': 0,
                'partially_correct': 0
            }

        stats = {
            'total_claims': len(line_by_line),
            'correct': 0,
            'incorrect': 0,
            'unverifiable': 0,
            'partially_correct': 0
        }

        for item in line_by_line:
            verdict = item.get('verdict', '').lower()
            if verdict == 'correct':
                stats['correct'] += 1
            elif verdict == 'incorrect':
                stats['incorrect'] += 1
            elif verdict == 'unverifiable':
                stats['unverifiable'] += 1
            elif verdict == 'partially correct':
                stats['partially_correct'] += 1

        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        line_by_line = evaluation_data.get('line_by_line', [])
        return pd.DataFrame(line_by_line)
