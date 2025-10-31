
import os
import json
from typing import Dict, List, Optional, Tuple, Any
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
                "OpenAI API key must be provided either as argument or in OPENAI_API_KEY environment variable")
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
        The reference article is:
        {reference_content}

        The AI-generated article is:
        {numbered_article}

        For each line in the AI-generated article, determine if it is:
        1. Correct (matches the reference article)
        2. Incorrect (contradicts the reference article)
        3. Missing (not present in the reference article)
        4. Additional (present in the AI-generated article but not in the reference)

        Return your evaluation as a JSON object with the following structure:
        {{
            "evaluation": [
                {{
                    "line_number": 1,
                    "line_text": "The line text from the AI-generated article",
                    "accuracy": "correct|incorrect|missing|additional",
                    "explanation": "Brief explanation of why this line was classified as such"
                }},
                ...
            ],
            "overall_accuracy": "high|medium|low",
            "confidence": "high|medium|low",
            "summary": "A brief summary of the evaluation"
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
        correct = sum(
            1 for item in evaluation_data['evaluation'] if item['accuracy'] == 'correct')
        incorrect = sum(
            1 for item in evaluation_data['evaluation'] if item['accuracy'] == 'incorrect')
        missing = sum(
            1 for item in evaluation_data['evaluation'] if item['accuracy'] == 'missing')
        additional = sum(
            1 for item in evaluation_data['evaluation'] if item['accuracy'] == 'additional')

        total_lines = len(evaluation_data['evaluation'])

        if total_lines == 0:
            return 0.0

        # Calculate a weighted score
        score = (correct - incorrect - missing - additional) / total_lines
        return max(-1.0, min(1.0, score))

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        correct = sum(
            1 for item in evaluation_data['evaluation'] if item['accuracy'] == 'correct')
        incorrect = sum(
            1 for item in evaluation_data['evaluation'] if item['accuracy'] == 'incorrect')
        missing = sum(
            1 for item in evaluation_data['evaluation'] if item['accuracy'] == 'missing')
        additional = sum(
            1 for item in evaluation_data['evaluation'] if item['accuracy'] == 'additional')

        total_lines = len(evaluation_data['evaluation'])

        return {
            'total_lines': total_lines,
            'correct': correct,
            'incorrect': incorrect,
            'missing': missing,
            'additional': additional,
            'correct_percentage': (correct / total_lines) * 100 if total_lines > 0 else 0,
            'incorrect_percentage': (incorrect / total_lines) * 100 if total_lines > 0 else 0,
            'missing_percentage': (missing / total_lines) * 100 if total_lines > 0 else 0,
            'additional_percentage': (additional / total_lines) * 100 if total_lines > 0 else 0
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        df = pd.DataFrame(evaluation_data['evaluation'])
        df['original_line'] = evaluation_data['original_lines']
        return df
