
import os
from typing import Optional, Dict, Any, Tuple, List
import openai
import pandas as pd
import re


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
            article = json_data[title]
            if isinstance(article, dict) and 'text' in article:
                return article['text']
            elif isinstance(article, str):
                return article
        # Try case-insensitive match
        for k, v in json_data.items():
            if k.lower() == title.lower():
                if isinstance(v, dict) and 'text' in v:
                    return v['text']
                elif isinstance(v, str):
                    return v
        return None

    def prepare_article_for_evaluation(self, article_content: str) -> Tuple[str, List[str]]:
        '''
        Prepare article for evaluation by cleaning and splitting into sentences.
        Returns the cleaned article and a list of sentences.
        '''
        if not isinstance(article_content, str):
            return "", []
        # Remove references, templates, and excessive whitespace
        cleaned = re.sub(r'\[\d+\]', '', article_content)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        # Split into sentences (simple split, can be improved)
        sentences = re.split(r'(?<=[.!?])\s+', cleaned)
        sentences = [s.strip() for s in sentences if s.strip()]
        return cleaned, sentences

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
        _, gen_sentences = self.prepare_article_for_evaluation(
            generated_article)
        _, ref_sentences = self.prepare_article_for_evaluation(
            reference_content)
        results = []
        for idx, sent in enumerate(gen_sentences):
            prompt = (
                "You are a Wikipedia fact-checker. "
                "Given the following reference article and a sentence from a generated article, "
                "determine if the sentence is factually accurate according to the reference. "
                "Reply with 'Correct', 'Incorrect', or 'Unverifiable', and briefly justify your answer.\n\n"
                f"Reference Article:\n{reference_content}\n\n"
                f"Generated Sentence:\n{sent}\n\n"
                "Your answer:"
            )
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=256,
                )
                content = response['choices'][0]['message']['content'].strip()
            except Exception as e:
                content = f"Error: {str(e)}"
            # Parse the result
            if content.lower().startswith("correct"):
                label = "Correct"
            elif content.lower().startswith("incorrect"):
                label = "Incorrect"
            elif content.lower().startswith("unverifiable"):
                label = "Unverifiable"
            else:
                # Try to extract label from the first word
                first_word = content.split()[0].capitalize()
                if first_word in ["Correct", "Incorrect", "Unverifiable"]:
                    label = first_word
                else:
                    label = "Unknown"
            results.append({
                "sentence_index": idx,
                "sentence": sent,
                "evaluation": label,
                "justification": content
            })
        return {
            "results": results,
            "reference_length": len(ref_sentences),
            "generated_length": len(gen_sentences)
        }

    def calculate_accuracy_score(self, evaluation_data: Dict) -> float:
        '''
        Calculate a normalized accuracy score from evaluation data.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            A score between -1 and 1 for compatibility with existing scoring
        '''
        results = evaluation_data.get("results", [])
        if not results:
            return 0.0
        correct = sum(1 for r in results if r["evaluation"] == "Correct")
        incorrect = sum(1 for r in results if r["evaluation"] == "Incorrect")
        unverifiable = sum(
            1 for r in results if r["evaluation"] == "Unverifiable")
        total = len(results)
        # Score: (correct - incorrect) / total, ignore unverifiable
        if total == 0:
            return 0.0
        score = (correct - incorrect) / total
        return max(-1.0, min(1.0, score))

    def calculate_accuracy_statistics(self, evaluation_data: Dict) -> Dict:
        '''
        Calculate statistics from the evaluation data.
        Args:
            evaluation_data: The line-by-line evaluation dictionary
        Returns:
            Dictionary with accuracy statistics
        '''
        results = evaluation_data.get("results", [])
        stats = {"total": len(results), "correct": 0,
                 "incorrect": 0, "unverifiable": 0, "unknown": 0}
        for r in results:
            label = r.get("evaluation", "Unknown")
            if label == "Correct":
                stats["correct"] += 1
            elif label == "Incorrect":
                stats["incorrect"] += 1
            elif label == "Unverifiable":
                stats["unverifiable"] += 1
            else:
                stats["unknown"] += 1
        if stats["total"] > 0:
            stats["accuracy"] = stats["correct"] / stats["total"]
        else:
            stats["accuracy"] = 0.0
        return stats

    def evaluation_to_dataframe(self, evaluation_data: Dict) -> pd.DataFrame:
        '''
        Convert evaluation data to a pandas DataFrame for easier analysis.
        Args:
            evaluation_data: The evaluation data from evaluate_article_accuracy
        Returns:
            DataFrame with evaluation results
        '''
        results = evaluation_data.get("results", [])
        df = pd.DataFrame(results)
        return df
