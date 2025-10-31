
from typing import Optional, Dict, Tuple, List, Any
import pandas as pd
from openai import OpenAI


class ArticleEvaluator:

    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4o'):
        if openai_api_key is None:
            raise ValueError("OpenAI API key is required")
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        for article in json_data.get('articles', []):
            if article.get('title') == title:
                return article.get('content')
        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        sentences = [sentence.strip()
                     for sentence in article_content.split('.') if sentence.strip()]
        return article_content, sentences

    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float = 0.2) -> Dict[str, Any]:
        reference, reference_sentences = self.prepare_article_for_evaluation(
            reference_content)
        generated, generated_sentences = self.prepare_article_for_evaluation(
            generated_article)

        evaluation_data = {'reference': reference,
                           'generated': generated, 'sentences': []}

        for sentence in generated_sentences:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a fact-checker. You will be given a reference article and a sentence from a generated article. Your task is to check if the sentence is factually accurate according to the reference article."},
                    {"role": "user", "content": f"Reference article: {reference}\nGenerated sentence: {sentence}\nIs the sentence factually accurate? Respond with 'True' or 'False' and a brief explanation."}
                ],
                temperature=temperature
            )
            result = response.choices[0].message.content.strip()
            try:
                accuracy, explanation = result.split(' ', 1)
                accuracy = accuracy.lower() == 'true'
            except ValueError:
                accuracy = None
                explanation = result
            evaluation_data['sentences'].append({
                'sentence': sentence,
                'accuracy': accuracy,
                'explanation': explanation
            })
        return evaluation_data

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        accurate_count = sum(
            1 for sentence in evaluation_data['sentences'] if sentence['accuracy'])
        total_count = len(evaluation_data['sentences'])
        return accurate_count / total_count if total_count > 0 else 0.0

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        accuracy_score = self.calculate_accuracy_score(evaluation_data)
        total_sentences = len(evaluation_data['sentences'])
        accurate_sentences = sum(
            1 for sentence in evaluation_data['sentences'] if sentence['accuracy'])
        inaccurate_sentences = total_sentences - accurate_sentences
        return {
            'accuracy_score': accuracy_score,
            'total_sentences': total_sentences,
            'accurate_sentences': accurate_sentences,
            'inaccurate_sentences': inaccurate_sentences
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        data = []
        for sentence_data in evaluation_data['sentences']:
            data.append({
                'sentence': sentence_data['sentence'],
                'accuracy': sentence_data['accuracy'],
                'explanation': sentence_data['explanation']
            })
        return pd.DataFrame(data)
