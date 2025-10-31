
import os
import json
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
            raise ValueError(
                "OpenAI API key not provided and OPENAI_API_KEY environment variable not set")
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
        for article in json_data:
            if article['title'] == title:
                return article['text']
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
        numbered_article = '\n'.join(numbered_lines)
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
        prompt = f"""
        Evaluate the factual accuracy of the following AI-generated Wikipedia article against the reference article.
        Reference Article:
        {reference_content}
        
        AI-Generated Article (line numbers for reference):
        {generated_article}
        
        For each line in the AI-generated article, provide a judgment on its factual accuracy based on the reference article.
        The judgment should be one of: 'Correct', 'Incorrect', 'Unverifiable', or 'Not Relevant'.
        Provide the judgment in JSON format with the line number as the key.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        try:
            evaluation_data = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            evaluation_data = {}
        return {'evaluation': evaluation_data, 'raw_response': response}

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        judgments = evaluation_data['evaluation']
        correct_count = sum(
            1 for judgment in judgments.values() if judgment == 'Correct')
        incorrect_count = sum(
            1 for judgment in judgments.values() if judgment == 'Incorrect')
        total_count = len(judgments)
        if total_count == 0:
            return 0
        score = (correct_count - incorrect_count) / total_count
        return score

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        judgments = evaluation_data['evaluation']
        statistics = {
            'total_lines': len(judgments),
            'correct': sum(1 for judgment in judgments.values() if judgment == 'Correct'),
            'incorrect': sum(1 for judgment in judgments.values() if judgment == 'Incorrect'),
            'unverifiable': sum(1 for judgment in judgments.values() if judgment == 'Unverifiable'),
            'not_relevant': sum(1 for judgment in judgments.values() if judgment == 'Not Relevant')
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
        judgments = evaluation_data['evaluation']
        data = [{'line_number': line_number, 'judgment': judgment}
                for line_number, judgment in judgments.items()]
        df = pd.DataFrame(data)
        return df
