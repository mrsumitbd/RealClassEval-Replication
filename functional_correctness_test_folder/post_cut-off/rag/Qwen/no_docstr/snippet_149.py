
import os
import openai
import pandas as pd
from typing import Optional, Dict, Any, Tuple, List


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
        return json_data.get(title)

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
        prompt = f"Please evaluate the factual accuracy of the following AI-generated Wikipedia article against the reference article. Provide a line-by-line evaluation indicating whether each line is accurate, inaccurate, or neutral.\n\nReference Article:\n{reference_content}\n\nAI-Generated Article:\n{generated_article}"
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=1500
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
        lines = evaluation_data.split('\n')
        accuracy_count = 0
        total_count = 0
        for line in lines:
            if 'accurate' in line.lower():
                accuracy_count += 1
            elif 'inaccurate' in line.lower():
                accuracy_count -= 1
            total_count += 1
        return (accuracy_count / total_count) if total_count > 0 else 0

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        lines = evaluation_data.split('\n')
        accurate_count = 0
        inaccurate_count = 0
        neutral_count = 0
        for line in lines:
            if 'accurate' in line.lower():
                accurate_count += 1
            elif 'inaccurate' in line.lower():
                inaccurate_count += 1
            elif 'neutral' in line.lower():
                neutral_count += 1
        return {
            'accurate': accurate_count,
            'inaccurate': inaccurate_count,
            'neutral': neutral_count,
            'total': len(lines)
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        lines = evaluation_data.split('\n')
        data = []
        for line in lines:
            parts = line.split('. ', 1)
            if len(parts) == 2:
                line_number, evaluation = parts
                data.append({'Line Number': int(line_number),
                            'Evaluation': evaluation.strip()})
        return pd.DataFrame(data)
