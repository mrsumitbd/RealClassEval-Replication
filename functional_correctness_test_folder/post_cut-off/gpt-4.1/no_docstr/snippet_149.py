
from typing import Optional, Dict, Any, Tuple, List
import pandas as pd
import openai


class ArticleEvaluator:

    def __init__(self, openai_api_key: Optional[str] = None, model: str = 'gpt-4o'):
        self.api_key = openai_api_key
        self.model = model
        if self.api_key:
            openai.api_key = self.api_key

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        # Assumes json_data is a dict with a list of articles, each with a 'title' and 'content'
        articles = json_data.get('articles', [])
        for article in articles:
            if article.get('title', '').strip().lower() == title.strip().lower():
                return article.get('content')
        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        # Returns the article and a list of sentences (split by period)
        sentences = [s.strip()
                     for s in article_content.split('.') if s.strip()]
        return article_content, sentences

    def evaluate_article_accuracy(self, reference_content: str, generated_article: str, temperature: float = 0.2) -> Dict[str, Any]:
        # Uses OpenAI API to compare reference and generated article, returns evaluation dict
        prompt = (
            "You are an expert fact-checker. Compare the following reference article and generated article. "
            "For each factual statement in the generated article, determine if it is accurate (matches the reference), "
            "partially accurate, or inaccurate. Return a JSON list of objects with 'statement', 'accuracy' "
            "(one of 'accurate', 'partially accurate', 'inaccurate'), and a brief 'explanation'.\n\n"
            "Reference Article:\n"
            f"{reference_content}\n\n"
            "Generated Article:\n"
            f"{generated_article}\n\n"
            "Output:"
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=1024,
        )
        import json
        content = response['choices'][0]['message']['content']
        # Try to extract JSON from the response
        try:
            start = content.find('[')
            end = content.rfind(']')
            eval_json = content[start:end+1]
            evaluation = json.loads(eval_json)
        except Exception:
            evaluation = []
        return {
            "reference": reference_content,
            "generated": generated_article,
            "evaluation": evaluation
        }

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        # Returns the proportion of 'accurate' statements
        evaluation = evaluation_data.get("evaluation", [])
        if not evaluation:
            return 0.0
        accurate = sum(1 for item in evaluation if item.get(
            'accuracy') == 'accurate')
        return accurate / len(evaluation)

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        # Returns counts of each accuracy type
        evaluation = evaluation_data.get("evaluation", [])
        stats = {"accurate": 0, "partially accurate": 0, "inaccurate": 0}
        for item in evaluation:
            acc = item.get('accuracy')
            if acc in stats:
                stats[acc] += 1
        stats['total'] = len(evaluation)
        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        # Converts evaluation list to DataFrame
        evaluation = evaluation_data.get("evaluation", [])
        df = pd.DataFrame(evaluation)
        return df
