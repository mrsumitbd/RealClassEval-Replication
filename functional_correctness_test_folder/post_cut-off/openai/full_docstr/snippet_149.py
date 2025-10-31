
import os
import json
from typing import Optional, Dict, Any, Tuple, List
import pandas as pd

try:
    import openai
except ImportError:
    openai = None  # pragma: no cover


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
        if openai is None:  # pragma: no cover
            raise ImportError(
                "openai package is required for ArticleEvaluator")
        self.model = model
        self.api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key must be provided either as argument or OPENAI_API_KEY env var")
        openai.api_key = self.api_key

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        '''
        Retrieve reference article text from the JSON data.
        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve
        Returns:
            The plain text content of the reference article, or None if not found
        '''
        # Support two common structures:
        # 1. dict of title -> content
        # 2. list of dicts with 'title' and 'text' or 'content'
        if isinstance(json_data, dict):
            return json_data.get(title)
        if isinstance(json_data, list):
            for entry in json_data:
                if entry.get('title') == title:
                    return entry.get('text') or entry.get('content')
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
        lines = article_content.splitlines()
        numbered_lines = [f"{idx + 1}. {line}" for idx,
                          line in enumerate(lines)]
        numbered_text = "\n".join(numbered_lines)
        return numbered_text, lines

    def evaluate_article_accuracy(
        self,
        reference_content: str,
        generated_article: str,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
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

        prompt = (
            "You are a Wikipedia fact-checker. Compare the following AI-generated article "
            "to the reference Wikipedia article. For each numbered line in the AI article, "
            "state whether the information is:\n"
            "1. Accurate\n"
            "2. Partially accurate\n"
            "3. Inaccurate\n"
            "4. Not present in the reference\n"
            "Provide the result as a JSON array of objects with keys:\n"
            "  - line_number (int)\n"
            "  - content (string)\n"
            "  - accuracy (string, one of 'accurate', 'partial', 'inaccurate', 'missing')\n"
            "  - confidence (float 0-1)\n"
            "Example:\n"
            "[{\"line_number\":1,\"content\":\"...\",\"accuracy\":\"accurate\",\"confidence\":0.95}, ...]\n\n"
            f"Reference article:\n{reference_content}\n\n"
            f"AI-generated article:\n{numbered_article}\n"
        )

        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        content = response.choices[0].message.content.strip()
        try:
            eval_data = json.loads(content)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from the response
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end != -1:
                try:
                    eval_data = json.loads(content[start:end])
                except Exception:
                    eval_data = {"error": "Failed to parse evaluation JSON"}
            else:
                eval_data = {"error": "Failed to parse evaluation JSON"}

        return {"line_evaluations": eval_data, "original_lines": original_lines}

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        line_evals = evaluation_data.get("line_evaluations", [])
        if not line_evals:
            return 0.0

        # Map accuracy strings to numeric scores
        score_map = {
            "accurate": 1.0,
            "partial": 0.0,
            "inaccurate": -1.0,
            "missing": -0.5,
        }

        scores = []
        for item in line_evals:
            acc = item.get("accuracy", "").lower()
            scores.append(score_map.get(acc, 0.0))

        # Normalize to [-1, 1]
        avg_score = sum(scores) / len(scores)
        # Clamp to [-1, 1]
        return max(-1.0, min(1.0, avg_score))

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        line_evals = evaluation_data.get("line_evaluations", [])
        stats = {
            "total_lines": len(line_evals),
            "accurate": 0,
            "partial": 0,
            "inaccurate": 0,
            "missing": 0,
            "accuracy_rate": 0.0,
        }
        for item in line_evals:
            acc = item.get("accuracy", "").lower()
            if acc in stats:
                stats[acc] += 1

        if stats["total_lines"] > 0:
            stats["accuracy_rate"] = (
                stats["accurate"] + 0.5 * stats["partial"]
            ) / stats["total_lines"]

        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        line_evals = evaluation_data.get("line_evaluations", [])
        if not line_evals:
            return pd.DataFrame()

        df = pd.DataFrame(line_evals)
        # Ensure consistent column order
