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
        # Try direct lookup
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
        system_prompt = (
            "You are a Wikipedia expert. Given a reference Wikipedia article and an AI-generated article, "
            "evaluate the factual accuracy of each line in the AI-generated article. "
            "For each line, respond with one of: 'accurate', 'inaccurate', or 'uncertain'. "
            "If inaccurate, briefly explain why. "
            "Return your answer as a JSON list of objects, one per line, with keys: "
            "'line_number', 'text', 'accuracy' (accurate/inaccurate/uncertain), and 'explanation' (if any)."
        )
        user_prompt = (
            f"Reference article:\n{reference_content}\n\n"
            f"AI-generated article (numbered lines):\n{numbered_text}\n\n"
            "Evaluate each line as described."
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=2048,
        )
        content = response['choices'][0]['message']['content']
        # Try to extract JSON from the response
        try:
            # Find the first and last curly braces to extract JSON
            start = content.find('[')
            end = content.rfind(']')
            if start != -1 and end != -1:
                json_str = content[start:end+1]
                eval_data = json.loads(json_str)
            else:
                eval_data = json.loads(content)
        except Exception:
            eval_data = []
        # Build a dict with all relevant info
        return {
            "lines": lines,
            "numbered_text": numbered_text,
            "evaluation": eval_data,
            "raw_response": content,
            "reference_content": reference_content,
            "generated_article": generated_article,
        }

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        eval_list = evaluation_data.get("evaluation", [])
        if not eval_list:
            return 0.0
        accurate = sum(1 for e in eval_list if str(
            e.get("accuracy", "")).lower() == "accurate")
        inaccurate = sum(1 for e in eval_list if str(
            e.get("accuracy", "")).lower() == "inaccurate")
        uncertain = sum(1 for e in eval_list if str(
            e.get("accuracy", "")).lower() == "uncertain")
        total = accurate + inaccurate + uncertain
        if total == 0:
            return 0.0
        # Score: (accurate - inaccurate) / total, so -1 to 1
        score = (accurate - inaccurate) / total
        return score

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        eval_list = evaluation_data.get("evaluation", [])
        accurate = sum(1 for e in eval_list if str(
            e.get("accuracy", "")).lower() == "accurate")
        inaccurate = sum(1 for e in eval_list if str(
            e.get("accuracy", "")).lower() == "inaccurate")
        uncertain = sum(1 for e in eval_list if str(
            e.get("accuracy", "")).lower() == "uncertain")
        total = len(eval_list)
        score = self.calculate_accuracy_score(evaluation_data)
        return {
            "total_lines": total,
            "accurate": accurate,
            "inaccurate": inaccurate,
            "uncertain": uncertain,
            "accuracy_score": score
        }

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        eval_list = evaluation_data.get("evaluation", [])
        df = pd.DataFrame(eval_list)
        return df
