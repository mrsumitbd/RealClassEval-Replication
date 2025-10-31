
from typing import Optional, Dict, List, Tuple, Any
import openai
import pandas as pd


class ArticleEvaluator:

    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4'):
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
        cleaned_sentences = [sentence.strip()
                             for sentence in sentences if sentence.strip()]
        return article_content, cleaned_sentences

    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float = 0.2) -> Dict[str, Any]:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an evaluator for article accuracy."},
                {"role": "user", "content": f"Reference Article: {reference_content}\nGenerated Article: {generated_article}"},
                {"role": "assistant", "content": "Evaluate the accuracy of the generated article compared to the reference article."}
            ],
            temperature=temperature
        )
        evaluation = response['choices'][0]['message']['content']
        return {'evaluation': evaluation}

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        # Assuming the evaluation contains a score in a specific format
        evaluation_text = evaluation_data.get('evaluation', '')
        if 'score' in evaluation_text:
            try:
                return float(evaluation_text.split('score:')[1].split()[0])
            except (IndexError, ValueError):
                pass
        return 0.0

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        # Assuming the evaluation contains statistics in a specific format
        evaluation_text = evaluation_data.get('evaluation', '')
        stats = {}
        if 'statistics' in evaluation_text:
            try:
                stats_lines = evaluation_text.split('statistics:')[
                    1].split('\n')
                for line in stats_lines:
                    if ': ' in line:
                        key, value = line.split(': ')
                        stats[key.strip()] = float(value.strip())
            except (IndexError, ValueError):
                pass
        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        data = {
            'evaluation': [evaluation_data.get('evaluation', '')],
            'score': [self.calculate_accuracy_score(evaluation_data)],
            **self.calculate_accuracy_statistics(evaluation_data)
        }
        return pd.DataFrame(data)
