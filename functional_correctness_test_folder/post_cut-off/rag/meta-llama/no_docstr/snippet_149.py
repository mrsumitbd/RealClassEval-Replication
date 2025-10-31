
import os
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import openai


class ArticleEvaluator:
    """
    A class to evaluate the factual accuracy of AI-generated Wikipedia articles
    against reference articles using OpenAI models.
    """

    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4o'):
        """
        Initialize the ArticleEvaluator with API credentials and model settings.
        Args:
            openai_api_key: API key for OpenAI (falls back to OPENAI_API_KEY env var)
            model: The OpenAI model to use for evaluation (default: gpt-4o)
        """
        self.openai_api_key = openai_api_key or os.environ.get(
            'OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError(
                "OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")

        openai.api_key = self.openai_api_key
        self.model = model

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        """
        Retrieve reference article text from the JSON data.
        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve
        Returns:
            The plain text content of the reference article, or None if not found
        """
        for article in json_data.get('articles', []):
            if article.get('title') == title:
                return article.get('text')
        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        """
        Prepare an AI-generated article for evaluation by numbering its lines.
        Args:
            article_content: The content of the AI-generated article
        Returns:
            A tuple containing:
            - Numbered article text suitable for the prompt
            - List of the original lines for further processing
        """
        lines = article_content.split('\n')
        numbered_lines = [f"{i+1}: {line}" for i, line in enumerate(lines)]
        numbered_article = '\n'.join(numbered_lines)
        return numbered_article, lines

    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float = 0.2) -> Dict[str, Any]:
        """
        Evaluate the factual accuracy of an AI-generated article against a reference.
        Args:
            reference_content: The text of the reference Wikipedia article
            generated_article: The text of the AI-generated article
            temperature: The sampling temperature for the OpenAI API call
        Returns:
            Dictionary containing the evaluation results
        """
        prompt = f"""Evaluate the factual accuracy of the following AI-generated Wikipedia article against the reference article. 
        Reference article: {reference_content}
        AI-generated article (with line numbers): {generated_article}
        
        For each line in the AI-generated article, determine if it is factually accurate compared to the reference article. 
        If a line is accurate, mark it as 'ACCURATE'. If it's inaccurate or contains information not present in the reference, 
        mark it as 'INACCURATE' and provide a brief explanation. If the line is a section header or doesn't contain factual information, 
        mark it as 'NON_FACTUAL'. Return the results as a JSON object with line numbers as keys and the evaluation as values.
        
        Format your response as: {{
            "line_evaluations": {{
                "1": {{"accuracy": "ACCURATE/INACCURATE/NON_FACTUAL", "explanation": "brief explanation if INACCURATE"}},
                "2": {{"accuracy": "ACCURATE/INACCURATE/NON_FACTUAL", "explanation": "brief explanation if INACCURATE"}},
                ...
            }},
            "overall_accuracy": "ACCURATE/INACCURATE/PARTIALLY_ACCURATE",
            "explanation": "overall explanation of the article's accuracy"
        }}"""

        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            response_format={"type": "json_object"}
        )

        try:
            evaluation_data = response.choices[0].message.content
            # Using eval here for simplicity; consider using json.loads for safer parsing
            return eval(evaluation_data)
        except Exception as e:
            print(f"Error parsing evaluation response: {e}")
            return {}

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        """
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        """
        line_evaluations = evaluation_data.get('line_evaluations', {})
        accurate_count = sum(1 for eval in line_evaluations.values(
        ) if eval.get('accuracy') == 'ACCURATE')
        inaccurate_count = sum(1 for eval in line_evaluations.values(
        ) if eval.get('accuracy') == 'INACCURATE')
        total_fact_count = accurate_count + inaccurate_count

        if total_fact_count == 0:
            return 0  # Avoid division by zero

        score = (accurate_count - inaccurate_count) / total_fact_count
        return score

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        """
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        """
        line_evaluations = evaluation_data.get('line_evaluations', {})
        stats = {
            'total_lines': len(line_evaluations),
            'accurate_lines': sum(1 for eval in line_evaluations.values() if eval.get('accuracy') == 'ACCURATE'),
            'inaccurate_lines': sum(1 for eval in line_evaluations.values() if eval.get('accuracy') == 'INACCURATE'),
            'non_factual_lines': sum(1 for eval in line_evaluations.values() if eval.get('accuracy') == 'NON_FACTUAL')
        }
        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        """
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        """
        line_evaluations = evaluation_data.get('line_evaluations', {})
        data = [
            {'line_number': line, **eval_data}
            for line, eval_data in line_evaluations.items()
        ]
        df = pd.DataFrame(data)
        return df
