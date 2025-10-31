
import os
import json
from typing import Optional, Dict, Any, Tuple, List
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
        for article in json_data.get('articles', []):
            if article.get('title') == title:
                return article.get('text')
        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        '''
        Prepare the article content for evaluation by splitting it into sections.
        Args:
            article_content: The text of the article to prepare
        Returns:
            A tuple containing the full article text and a list of section texts
        '''
        sections = article_content.split('\n\n')
        return article_content, sections

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
        You are an expert evaluator of Wikipedia articles. Your task is to compare the generated article with the reference article and evaluate the factual accuracy of the generated article.

        Reference Article:
        {reference_content}

        Generated Article:
        {generated_article}

        Please provide a line-by-line comparison of the generated article against the reference article, indicating whether each line is accurate, inaccurate, or not applicable. Also, provide an overall accuracy score between -1 and 1, where -1 is completely inaccurate and 1 is completely accurate.

        Format your response as a JSON object with the following structure:
        {{
            "line_by_line_evaluation": [
                {{
                    "line_number": int,
                    "generated_line": str,
                    "reference_line": str,
                    "accuracy": "accurate" | "inaccurate" | "not_applicable",
                    "explanation": str
                }},
                ...
            ],
            "overall_accuracy": float,
            "summary": str
        }}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
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
        return evaluation_data.get('overall_accuracy', 0.0)

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        line_by_line = evaluation_data.get('line_by_line_evaluation', [])
        total_lines = len(line_by_line)
        accurate_lines = sum(
            1 for line in line_by_line if line.get('accuracy') == 'accurate')
        inaccurate_lines = sum(
            1 for line in line_by_line if line.get('accuracy') == 'inaccurate')
        not_applicable_lines = sum(
            1 for line in line_by_line if line.get('accuracy') == 'not_applicable')

        statistics = {
            'total_lines': total_lines,
            'accurate_lines': accurate_lines,
            'inaccurate_lines': inaccurate_lines,
            'not_applicable_lines': not_applicable_lines,
            'accuracy_rate': accurate_lines / total_lines if total_lines > 0 else 0.0,
            'inaccuracy_rate': inaccurate_lines / total_lines if total_lines > 0 else 0.0,
            'not_applicable_rate': not_applicable_lines / total_lines if total_lines > 0 else 0.0
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
        line_by_line = evaluation_data.get('line_by_line_evaluation', [])
        df = pd.DataFrame(line_by_line)
        return df
