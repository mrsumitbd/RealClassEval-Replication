
import os
import json
from typing import Optional, Dict, Any, Tuple, List
import pandas as pd
import openai


class ArticleEvaluator:
    """
    A class to evaluate the factual accuracy of AI-generated Wikipedia articles
    against reference articles using OpenAI models.
    """

    def __init__(self, openai_api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialize the ArticleEvaluator with API credentials and model settings.

        Args:
            openai_api_key: API key for OpenAI (falls back to OPENAI_API_KEY env var)
            model: The OpenAI model to use for evaluation (default: gpt-4o)
        """
        self.model = model
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key must be provided either as argument or OPENAI_API_KEY env var")
        openai.api_key = self.api_key

    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        """
        Retrieve reference article text from the JSON data.

        Args:
            json_data: The loaded JSON data with Wikipedia articles
            title: The title of the article to retrieve

        Returns:
            The plain text content of the reference article, or None if not found
        """
        # Support two common structures:
        # 1. {"articles": [{"title": "...", "content": "..."}]}
        # 2. {"title": "...", "content": "..."}  (single article)
        if isinstance(json_data, dict):
            # Case 2
            if json_data.get("title") == title:
                return json_data.get("content") or json_data.get("text")
            # Case 1
            articles = json_data.get("articles", [])
            for art in articles:
                if art.get("title") == title:
                    return art.get("content") or art.get("text")
        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        """
        Prepare article text for evaluation by normalizing whitespace and splitting into sentences.

        Args:
            article_content: Raw article text

        Returns:
            Tuple of cleaned article string and list of sentence strings
        """
        cleaned = " ".join(article_content.split())
        # Very simple sentence splitter: split on period followed by space or end of string
        sentences = [s.strip() for s in cleaned.split(".") if s.strip()]
        return cleaned, sentences

    def evaluate_article_accuracy(
        self,
        reference_content: str,
        generated_article: str,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        """
        Evaluate the factual accuracy of an AI-generated article against a reference.

        Args:
            reference_content: The text of the reference Wikipedia article
            generated_article: The text of the AI-generated article
            temperature: The sampling temperature for the OpenAI API call

        Returns:
            Dictionary containing the evaluation results
        """
        system_prompt = (
            "You are an expert Wikipedia fact-checker. "
            "Compare the reference article with the generated article. "
            "For each sentence in the generated article, determine if it is factually correct "
            "with respect to the reference. "
            "Return a JSON object with the following structure:\n"
            "{\n"
            "  \"overall_accuracy\": float between 0 and 1,\n"
            "  \"sentence_evaluations\": [\n"
            "    {\n"
            "      \"generated_sentence\": \"...\",\n"
            "      \"reference_sentence\": \"...\",\n"
            "      \"accuracy\": float between 0 and 1,\n"
            "      \"comment\": \"...\"\n"
            "    },\n"
            "    ...\n"
            "  ]\n"
            "}"
        )
        user_prompt = (
            f"Reference Article:\n{reference_content}\n\n"
            f"Generated Article:\n{generated_article}\n\n"
            "Please evaluate as described."
        )

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            content = response.choices[0].message.content.strip()
            # Try to parse JSON; if fails, return raw content
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                data = {"raw_response": content}
            return data
        except Exception as e:
            return {"error": str(e)}

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        """
        Calculate a normalized accuracy score from evaluation data.

        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy

        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        """
        if "sentence_evaluations" not in evaluation_data:
            return 0.0
        accuracies = [s.get("accuracy", 0)
                      for s in evaluation_data["sentence_evaluations"]]
        if not accuracies:
            return 0.0
        mean_acc = sum(accuracies) / len(accuracies)
        # Map 0-1 to -1 to 1
        return 2 * mean_acc - 1

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        """
        Calculate statistics from the evaluation data.

        Args:
            evaluation_data: The line-by-line evaluation dictionary

        Returns:
            Dictionary with accuracy statistics
        """
        if "sentence_evaluations" not in evaluation_data:
            return {}
        accuracies = [s.get("accuracy", 0)
                      for s in evaluation_data["sentence_evaluations"]]
        if not accuracies:
            return {}
        stats = {
            "count": len(accuracies),
            "mean_accuracy": sum(accuracies) / len(accuracies),
            "min_accuracy": min(accuracies),
            "max_accuracy": max(accuracies),
            "std_accuracy": (
                (sum((x - (sum(accuracies) / len(accuracies)))
                 ** 2 for x in accuracies) / len(accuracies))
                ** 0.5
            ),
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
        if "sentence_evaluations" not in evaluation_data:
            return pd.DataFrame()
        df = pd.DataFrame(evaluation_data["sentence_evaluations"])
        # Add overall accuracy as a column if present
        if "overall_accuracy" in evaluation_data:
            df["overall_accuracy"] = evaluation_data["overall_accuracy"]
        return df
