
import os
import json
from typing import Optional, Dict, List, Tuple, Any
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
        for article in json_data['articles']:
            if article['title'] == title:
                return article['content']
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
        numbered_lines = [f"{i+1}. {line}" for i, line in enumerate(lines)]
        numbered_text = '\n'.join(numbered_lines)
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

        prompt = f"""
        You are an expert evaluator of Wikipedia articles. Your task is to evaluate the factual accuracy of an AI-generated article against a reference article.

        Reference Article:
        {reference_content}

        AI-Generated Article:
        {numbered_text}

        Please evaluate each line of the AI-generated article and provide a score between -1 and 1, where:
        -1: Completely incorrect or misleading information
        -0.5: Partially correct but with significant inaccuracies
        0: Neutral or no clear factual information
        0.5: Mostly correct but with minor inaccuracies
        1: Completely correct and accurate

        Provide your evaluation in the following JSON format:
        {{
            "evaluation": [
                {{
                    "line_number": 1,
                    "line_content": "Line 1 content",
                    "score": 0.5,
                    "explanation": "Explanation for the score"
                }},
                ...
            ],
            "overall_score": 0.5,
            "overall_explanation": "Overall explanation for the score"
        }}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",
                    "content": "You are an expert evaluator of Wikipedia articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        evaluation_data = json.loads(response.choices[0].message.content)
        return evaluation_data

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        total_score = sum(item['score']
                          for item in evaluation_data['evaluation'])
        num_lines = len(evaluation_data['evaluation'])
        return total_score / num_lines if num_lines > 0 else 0

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        scores = [item['score'] for item in evaluation_data['evaluation']]
        statistics = {
            'mean': sum(scores) / len(scores),
            'max': max(scores),
            'min': min(scores),
            'correct_lines': sum(1 for score in scores if score >= 0.5),
            'incorrect_lines': sum(1 for score in scores if score < 0.5),
            'total_lines': len(scores)
        }
        return statistics

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        df = pd.DataFrame(evaluation_data['evaluation'])
        df['overall_score'] = evaluation_data['overall_score']
        df['overall_explanation'] = evaluation_data['overall_explanation']
        return df
