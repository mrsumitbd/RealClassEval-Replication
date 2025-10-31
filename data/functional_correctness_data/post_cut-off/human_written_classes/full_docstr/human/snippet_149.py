from typing import Any, Dict, List, Optional, Tuple
import re
import yaml
import pandas as pd
import os

class ArticleEvaluator:
    """
    A class to evaluate the factual accuracy of AI-generated Wikipedia articles
    against reference articles using OpenAI models.
    """

    def __init__(self, openai_api_key: Optional[str]=None, model: str='gpt-4o'):
        """
        Initialize the ArticleEvaluator with API credentials and model settings.

        Args:
            openai_api_key: API key for OpenAI (falls back to OPENAI_API_KEY env var)
            model: The OpenAI model to use for evaluation (default: gpt-4o)
        """
        self.api_key = openai_api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError('OpenAI API key not provided. Set OPENAI_API_KEY environment variable.')
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        logger.info(f'ArticleEvaluator initialized with model: {model}')

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        """
        Retrieve reference article text from the JSON data.

        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve

        Returns:
            The plain text content of the reference article, or None if not found
        """
        for article in json_data:
            if article.get('title', '').lower() == title.lower():
                return article.get('plain_text', '')
        for article in json_data:
            if title.lower() in article.get('title', '').lower():
                logger.info(f"Found partial title match: '{article.get('title')}' for query '{title}'")
                return article.get('plain_text', '')
        logger.warning(f'No reference article found for title: {title}')
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
        article_content = article_content.strip()
        paragraphs = [p for p in article_content.split('\n\n') if p.strip()]
        numbered_lines = []
        original_lines = []
        line_number = 1
        for paragraph in paragraphs:
            if len(paragraph.strip()) < 3:
                continue
            numbered_lines.append(f'{line_number}: {paragraph}')
            original_lines.append(paragraph)
            line_number += 1
        numbered_text = '\n\n'.join(numbered_lines)
        logger.info(f'Prepared article with {len(original_lines)} numbered lines')
        return (numbered_text, original_lines)

    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float=0.2) -> Dict[str, Any]:
        """
        Evaluate the factual accuracy of an AI-generated article against a reference.

        Args:
            reference_content: The text of the reference Wikipedia article
            generated_article: The text of the AI-generated article
            temperature: The sampling temperature for the OpenAI API call

        Returns:
            Dictionary containing the evaluation results
        """
        numbered_article, original_lines = self.prepare_article_for_evaluation(generated_article)
        prompt = f"""\nYou are an expert fact-checker comparing an AI-generated article with a reference Wikipedia article.\n\n# Classification Criteria\n- CORRECT: The statement is accurate and verifiable in the reference article\n- INCORRECT: The statement contradicts information in the reference article\n- UNKNOWN: The reference doesn't mention this information or provides insufficient details to verify\n\n# Output Format\nYou must produce valid YAML with this exact structure for each numbered line:\n1:\n  analysis: "Brief analysis of line 1"\n  accuracy: "CORRECT|INCORRECT|UNKNOWN"\n2:\n  analysis: "Brief analysis of line 2"\n  accuracy: "CORRECT|INCORRECT|UNKNOWN"\n...\n\n# REFERENCE ARTICLE:\n{reference_content}\n\n# AI-GENERATED ARTICLE (NUMBERED LINES):\n{numbered_article}\n"""
        try:
            logger.warning('Evaluating article factual accuracy...')
            response = self.client.chat.completions.create(model=self.model, messages=[{'role': 'system', 'content': 'You are a precision fact-checker that produces only valid YAML.'}, {'role': 'user', 'content': prompt}], temperature=temperature)
            yaml_content = response.choices[0].message.content
            yaml_pattern = '```(?:yaml)?\\s*([\\s\\S]*?)\\s*```'
            yaml_match = re.search(yaml_pattern, yaml_content)
            if yaml_match:
                yaml_content = yaml_match.group(1)
            try:
                logger.warning('Parsing evaluation results...')
                evaluation_data = yaml.safe_load(yaml_content)
                if not isinstance(evaluation_data, dict):
                    logger.error(f'Evaluation did not return a dictionary: {evaluation_data}')
                    return {'error': 'Invalid evaluation format', 'raw_response': yaml_content}
                stats = self.calculate_accuracy_statistics(evaluation_data)
                return {'evaluation': evaluation_data, 'statistics': stats, 'lines_count': len(original_lines), 'evaluated_lines_count': len(evaluation_data)}
            except yaml.YAMLError as e:
                logger.error(f'Failed to parse YAML response: {e}')
                return {'error': f'Failed to parse YAML response: {e}', 'raw_response': yaml_content}
        except Exception as e:
            logger.error(f'API call failed: {e}')
            return {'error': f'API call failed: {e}'}

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        """
        Calculate a normalized accuracy score from evaluation data.

        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy

        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        """
        if not evaluation_data or 'evaluation' not in evaluation_data:
            return 0.0
        evaluation = evaluation_data['evaluation']
        total_lines = len(evaluation)
        if total_lines == 0:
            return 0.0
        correct_count = sum((1 for item in evaluation.values() if item.get('accuracy', '') == 'CORRECT'))
        incorrect_count = sum((1 for item in evaluation.values() if item.get('accuracy', '') == 'INCORRECT'))
        pct_correct = correct_count / total_lines if total_lines > 0 else 0
        pct_incorrect = incorrect_count / total_lines if total_lines > 0 else 0
        score = pct_correct * 2 - 1 - pct_incorrect * 0.5
        return max(-1, min(1, score))

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        """
        Calculate statistics from the evaluation data.

        Args:
            evaluation_data: The line-by-line evaluation dictionary

        Returns:
            Dictionary with accuracy statistics
        """
        if not evaluation_data:
            return {'correct_count': 0, 'incorrect_count': 0, 'unknown_count': 0, 'total_count': 0, 'pct_correct': 0, 'pct_incorrect': 0, 'pct_unknown': 0}
        total_count = len(evaluation_data)
        correct_count = sum((1 for item in evaluation_data.values() if item.get('accuracy', '') == 'CORRECT'))
        incorrect_count = sum((1 for item in evaluation_data.values() if item.get('accuracy', '') == 'INCORRECT'))
        unknown_count = sum((1 for item in evaluation_data.values() if item.get('accuracy', '') == 'UNKNOWN'))
        pct_correct = correct_count / total_count * 100 if total_count > 0 else 0
        pct_incorrect = incorrect_count / total_count * 100 if total_count > 0 else 0
        pct_unknown = unknown_count / total_count * 100 if total_count > 0 else 0
        return {'correct_count': correct_count, 'incorrect_count': incorrect_count, 'unknown_count': unknown_count, 'total_count': total_count, 'pct_correct': pct_correct, 'pct_incorrect': pct_incorrect, 'pct_unknown': pct_unknown}

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        """
        Convert evaluation data to a pandas DataFrame for easier analysis.

        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy

        Returns:
            DataFrame with evaluation results
        """
        if not evaluation_data or 'evaluation' not in evaluation_data:
            return pd.DataFrame()
        evaluation = evaluation_data['evaluation']
        data = []
        for line_num, content in evaluation.items():
            data.append({'line_number': line_num, 'analysis': content.get('analysis', ''), 'accuracy': content.get('accuracy', 'UNKNOWN')})
        return pd.DataFrame(data)