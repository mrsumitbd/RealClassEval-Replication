
import os
from typing import Optional, Dict, List, Any, Tuple
import openai
import pandas as pd


class ArticleEvaluator:
    '''
    A class to evaluate the factual accuracy of AI-generated Wikipedia articles
    against reference articles using OpenAI models.
    '''

    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4'):
        '''
        Initialize the ArticleEvaluator with API credentials and model settings.
        Args:
            openai_api_key: API key for OpenAI (falls back to OPENAI_API_KEY env var)
            model: The OpenAI model to use for evaluation (default: gpt-4)
        '''
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        openai.api_key = self.openai_api_key
        self.model = model

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        '''
        Retrieve reference article text from the JSON data.
        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve
        Returns:
            The plain text content of the reference article, or None if not found
        '''
        return json_data.get(title, None)

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        '''
        Prepare the article content for evaluation by splitting it into sentences.
        Args:
            article_content: The text of the article to prepare
        Returns:
            A tuple containing the original article content and a list of sentences
        '''
        import re
        sentences = re.split(r'(?<=[.!?]) +', article_content)
        return article_content, sentences

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
        prompt = f"Compare the following AI-generated article to the reference article and provide a detailed evaluation of its factual accuracy. Return the result as a JSON object with keys 'accuracy', 'differences', and 'comments'.\n\nReference Article:\n{reference_content}\n\nGenerated Article:\n{generated_article}"
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=1024
        )
        return response.choices[0].text.strip()

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        accuracy = evaluation_data.get('accuracy', 0)
        return (accuracy - 50) / 50

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        differences = evaluation_data.get('differences', [])
        comments = evaluation_data.get('comments', '')
        return {
            'number_of_differences': len(differences),
            'comments_length': len(comments)
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        data = {
            'accuracy': [evaluation_data.get('accuracy', None)],
            'differences': [evaluation_data.get('differences', None)],
            'comments': [evaluation_data.get('comments', None)]
        }
        return pd.DataFrame(data)
