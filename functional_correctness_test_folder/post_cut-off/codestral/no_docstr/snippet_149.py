
import pandas as pd
from typing import Optional, Dict, Any, Tuple, List
from openai import OpenAI


class ArticleEvaluator:

    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4o'):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        for article in json_data.get('articles', []):
            if article.get('title') == title:
                return article.get('content')
        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        sentences = article_content.split('. ')
        return article_content, sentences

    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float = 0.2) -> Dict[str, Any]:
        prompt = f"""
        Evaluate the accuracy of the following generated article against the reference article.

        Reference Article:
        {reference_content}

        Generated Article:
        {generated_article}

        Provide the evaluation in the following JSON format:
        {{
            "accuracy_score": float,
            "correct_sentences": list,
            "incorrect_sentences": list,
            "missing_sentences": list,
            "extra_sentences": list
        }}
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        evaluation_data = response.choices[0].message.content
        return evaluation_data

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        return evaluation_data.get('accuracy_score', 0.0)

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        total_sentences = len(evaluation_data.get(
            'correct_sentences', [])) + len(evaluation_data.get('incorrect_sentences', []))
        statistics = {
            'total_sentences': total_sentences,
            'correct_sentences': len(evaluation_data.get('correct_sentences', [])),
            'incorrect_sentences': len(evaluation_data.get('incorrect_sentences', [])),
            'missing_sentences': len(evaluation_data.get('missing_sentences', [])),
            'extra_sentences': len(evaluation_data.get('extra_sentences', []))
        }
        return statistics

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        data = {
            'correct_sentences': evaluation_data.get('correct_sentences', []),
            'incorrect_sentences': evaluation_data.get('incorrect_sentences', []),
            'missing_sentences': evaluation_data.get('missing_sentences', []),
            'extra_sentences': evaluation_data.get('extra_sentences', [])
        }
        return pd.DataFrame(data)
