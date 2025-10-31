
import json
from typing import Any, Dict, List, Optional, Tuple

import openai
import pandas as pd


class ArticleEvaluator:
    """
    A helper class for evaluating generated articles against reference articles.
    """

    def __init__(self, openai_api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialise the evaluator.

        Parameters
        ----------
        openai_api_key : Optional[str]
            The OpenAI API key. If None, the key is taken from the environment.
        model : str
            The OpenAI model to use for evaluation.
        """
        if openai_api_key is not None:
            openai.api_key = openai_api_key
        self.model = model

    # ------------------------------------------------------------------
    # Reference article handling
    # ------------------------------------------------------------------
    def get_reference_article(self, json_data: Dict, title: str) -> Optional[str]:
        """
        Retrieve the content of a reference article by title.

        Parameters
        ----------
        json_data : Dict
            A dictionary containing article data. Expected to have a key
            'articles' which is a list of dicts with 'title' and 'content'.
        title : str
            The title of the article to retrieve.

        Returns
        -------
        Optional[str]
            The article content if found, otherwise None.
        """
        articles = json_data.get("articles", [])
        for article in articles:
            if article.get("title", "").lower() == title.lower():
                return article.get("content")
        return None

    # ------------------------------------------------------------------
    # Article preparation
    # ------------------------------------------------------------------
    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        """
        Prepare an article for evaluation.

        Parameters
        ----------
        article_content : str
            The raw article text.

        Returns
        -------
        Tuple[str, List[str]]
            The cleaned article text and a list of sentences.
        """
        # Basic cleaning: strip whitespace and collapse multiple spaces
        cleaned = " ".join(article_content.split())
        # Split into sentences (naïve split on period followed by space)
        sentences = [s.strip() for s in cleaned.split(". ") if s.strip()]
        return cleaned, sentences

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------
    def evaluate_article_accuracy(
        self,
        reference_content: str,
        generated_article: str,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        """
        Evaluate the accuracy of a generated article against a reference.

        Parameters
        ----------
        reference_content : str
            The reference article text.
        generated_article : str
            The generated article text.
        temperature : float
            Temperature for the OpenAI completion.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the score (0-1) and comments.
        """
        prompt = (
            "You are an expert editor. Compare the following reference article "
            "with the generated article. Rate the accuracy on a scale from 0 to 1 "
            "(1 = identical, 0 = completely different). Provide a brief comment "
            "explaining the score.\n\n"
            f"Reference article:\n{reference_content}\n\n"
            f"Generated article:\n{generated_article}\n\n"
            "Score and comment:"
        )

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=200,
        )

        text = response.choices[0].message.content.strip()

        # Try to parse score and comment
        score = 0.0
        comment = ""
        # Expect format: "Score: X\nComment: Y" or similar
        lines = text.splitlines()
        for line in lines:
            if line.lower().startswith("score"):
                try:
                    score = float(line.split(":")[1].strip())
                except Exception:
                    pass
            elif line.lower().startswith("comment"):
                comment = line.split(":", 1)[1].strip()
            else:
                # If no explicit labels, try to extract first number
                try:
                    score = float(line.split()[0])
                except Exception:
                    pass

        return {"score": score, "comment": comment, "reference": reference_content, "generated": generated_article}

    # ------------------------------------------------------------------
    # Scoring utilities
    # ------------------------------------------------------------------
    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        """
        Calculate the overall accuracy score from evaluation data.

        Parameters
        ----------
        evaluation_data : Dict
            The dictionary returned by `evaluate_article_accuracy`.

        Returns
        -------
        float
            The accuracy score (0-1).
        """
        return float(evaluation_data.get("score", 0.0))

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        """
        Calculate statistics from a list of evaluation data dictionaries.

        Parameters
        ----------
        evaluation_data : Dict
            A dictionary where each key is an article identifier and the value
            is the evaluation dictionary.

        Returns
        -------
        Dict
            Statistics: mean, std, min, max, count.
        """
        scores = [self.calculate_accuracy_score(
            v) for v in evaluation_data.values()]
        if not scores:
            return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "count": 0}
        import numpy as np

        arr = np.array(scores)
        return {
            "mean": float(arr.mean()),
            "std": float(arr.std()),
            "min": float(arr.min()),
            "max": float(arr.max()),
            "count": int(len(arr)),
        }

    # ------------------------------------------------------------------
    # DataFrame conversion
    # ------------------------------------------------------------------
    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        """
        Convert evaluation data into a pandas DataFrame.

        Parameters
        ----------
        evaluation_data : Dict
            A dictionary where each key is an article identifier and the value
            is the evaluation dictionary.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: id, score, comment, reference, generated.
        """
        rows = []
        for article_id, data in evaluation_data.items():
            row = {
                "id": article_id,
                "score": data.get("score"),
                "comment": data.get("comment"),
                "reference": data.get("reference"),
                "generated": data.get("generated"),
            }
            rows.append(row)
        return pd.DataFrame(rows)
