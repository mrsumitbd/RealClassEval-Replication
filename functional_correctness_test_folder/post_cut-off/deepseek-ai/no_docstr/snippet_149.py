
import openai
from typing import Optional, Dict, Tuple, List, Any
import pandas as pd
import json
from tenacity import retry, stop_after_attempt, wait_exponential


class ArticleEvaluator:

    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4o'):
        if openai_api_key:
            openai.api_key = openai_api_key
        self.model = model

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        for article in json_data.get('articles', []):
            if article.get('title') == title:
                return article.get('content')
        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        sentences = article_content.split('. ')
        main_content = article_content
        return main_content, sentences

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float = 0.2) -> Dict[str, Any]:
        prompt = f"""
        Compare the following reference article with the generated article and evaluate the accuracy of the generated article.
        
        Reference Article:
        {reference_content}
        
        Generated Article:
        {generated_article}
        
        Provide a detailed evaluation including:
        - Overall accuracy score (0-100)
        - List of factual inaccuracies (if any)
        - List of missing key points (if any)
        - List of misleading statements (if any)
        - General comments on the quality of the generated article
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert fact-checker and evaluator of articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        evaluation_text = response.choices[0].message['content']

        try:
            evaluation_data = json.loads(evaluation_text)
        except json.JSONDecodeError:
            evaluation_data = {
                "accuracy_score": None,
                "factual_inaccuracies": [],
                "missing_key_points": [],
                "misleading_statements": [],
                "comments": evaluation_text
            }

        return evaluation_data

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        return evaluation_data.get('accuracy_score', 0.0)

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        num_inaccuracies = len(evaluation_data.get('factual_inaccuracies', []))
        num_missing = len(evaluation_data.get('missing_key_points', []))
        num_misleading = len(evaluation_data.get('misleading_statements', []))

        return {
            'num_factual_inaccuracies': num_inaccuracies,
            'num_missing_key_points': num_missing,
            'num_misleading_statements': num_misleading,
            'accuracy_score': evaluation_data.get('accuracy_score', 0.0)
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        stats = self.calculate_accuracy_statistics(evaluation_data)
        df = pd.DataFrame([stats])
        return df
