import os
import json
from typing import Optional, Dict, Any, Tuple, List
import openai
import pandas as pd


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
        if openai_api_key is None:
            openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.openai_api_key = openai_api_key
        self.model = model
        openai.api_key = self.openai_api_key

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        '''
        Retrieve reference article text from the JSON data.
        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve
        Returns:
            The plain text content of the reference article, or None if not found
        '''
        if not isinstance(json_data, dict):
            return None
        # Try direct key
        if title in json_data:
            return json_data[title]
        # Try case-insensitive match
        for k, v in json_data.items():
            if k.lower() == title.lower():
                return v
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
                 for line in article_content.strip().split('\n') if line.strip()]
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
        numbered_text, lines = self.prepare_article_for_evaluation(
            generated_article)
        prompt = (
            "You are a fact-checking assistant. Given a reference Wikipedia article and an AI-generated article, "
            "evaluate each line of the AI-generated article for factual accuracy. "
            "For each line, respond with one of: 'accurate', 'inaccurate', or 'uncertain', and provide a brief justification. "
            "Return your answer as a JSON list of objects, each with keys: 'line_number', 'line', 'verdict', 'justification'.\n\n"
            "Reference Article:\n"
            f"{reference_content}\n\n"
            "AI-Generated Article (numbered lines):\n"
            f"{numbered_text}\n\n"
            "Evaluate each line as described."
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful and precise Wikipedia fact-checking assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=2048
        )
        content = response['choices'][0]['message']['content']
        # Try to parse JSON from the response
        try:
            # Find the first and last curly braces to extract JSON
            start = content.find('[')
            end = content.rfind(']')
            if start != -1 and end != -1:
                json_str = content[start:end+1]
                evaluation = json.loads(json_str)
            else:
                evaluation = json.loads(content)
        except Exception:
            evaluation = []
        return {
            "lines": lines,
            "numbered_text": numbered_text,
            "evaluation": evaluation,
            "raw_response": content
        }

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        evaluation = evaluation_data.get("evaluation", [])
        if not evaluation:
            return 0.0
        accurate = sum(1 for e in evaluation if str(
            e.get("verdict", "")).strip().lower() == "accurate")
        inaccurate = sum(1 for e in evaluation if str(
            e.get("verdict", "")).strip().lower() == "inaccurate")
        total = len(evaluation)
        if total == 0:
            return 0.0
        # Score: (accurate - inaccurate) / total, clipped to [-1, 1]
        score = (accurate - inaccurate) / total
        return max(-1.0, min(1.0, score))

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        evaluation = evaluation_data.get("evaluation", [])
        stats = {"accurate": 0, "inaccurate": 0, "uncertain": 0, "total": 0}
        for e in evaluation:
            verdict = str(e.get("verdict", "")).strip().lower()
            if verdict in stats:
                stats[verdict] += 1
            else:
                stats["uncertain"] += 1
            stats["total"] += 1
        if stats["total"] > 0:
            stats["accuracy_rate"] = stats["accurate"] / stats["total"]
            stats["inaccuracy_rate"] = stats["inaccurate"] / stats["total"]
            stats["uncertainty_rate"] = stats["uncertain"] / stats["total"]
        else:
            stats["accuracy_rate"] = 0.0
            stats["inaccuracy_rate"] = 0.0
            stats["uncertainty_rate"] = 0.0
        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        evaluation = evaluation_data.get("evaluation", [])
        df = pd.DataFrame(evaluation)
        return df
