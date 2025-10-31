"""
Few-shot prompt construction for LLM generation.
Single user message with all examples.
"""

from typing import List, Dict, Any
from pathlib import Path
import logging

from rag_retriever import RetrievedExample

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptBuilder:
    """Build few-shot prompts in OpenAI message format."""

    def __init__(self):
        """Initialize prompt builder."""
        pass

    def build_messages(self, target_skeleton: str,
                      examples: List[RetrievedExample]) -> List[Dict[str, str]]:
        """
        Build OpenAI-compatible messages with few-shot examples.

        Args:
            target_skeleton: Target class skeleton from v2
            examples: List of retrieved examples from v1

        Returns:
            List of message dictionaries (2 messages: assistant + user)
        """
        messages = []

        # Assistant message (system instruction)
        messages.append({
            "role": "assistant",
            "content": "You are an expert Python programmer who can correctly implement complete Python classes based on the provided class skeleton."
        })

        # Build the user message content with all examples
        user_content_parts = []

        # Add preamble if there are examples
        if examples:
            user_content_parts.append("For your understanding, following are some (skeleton, code) examples:\n")

        # Add each example
        for i, example in enumerate(examples, 1):
            user_content_parts.append(f"\nExample skeleton:\n\n{example.skeleton}")
            user_content_parts.append(f"\nCorresponding class implementation:\n\n{example.implementation}\n")

        # Add the target task
        user_content_parts.append(f"\nNow, implement the following class. Do not explain the code. The given class skeleton is as follows:\n{target_skeleton}")

        # Combine into single user message
        user_content = "".join(user_content_parts)

        messages.append({
            "role": "user",
            "content": user_content
        })

        return messages

    def build_messages_dict(self, target_skeleton: str,
                           examples: List[RetrievedExample]) -> Dict[str, Any]:
        """
        Build messages and return with metadata.

        Args:
            target_skeleton: Target class skeleton from v2
            examples: List of retrieved examples from v1

        Returns:
            Dictionary with messages and metadata
        """
        messages = self.build_messages(target_skeleton, examples)

        return {
            'messages': messages,
            'num_examples': len(examples),
            'num_messages': len(messages),
            'target_skeleton': target_skeleton,
            'example_info': [
                {
                    'class_name': ex.class_name,
                    'similarity_score': ex.similarity_score,
                    'index': ex.index
                }
                for ex in examples
            ]
        }

    def save_messages(self, messages: List[Dict[str, str]], output_path: str):
        """
        Save messages to JSON file.

        Args:
            messages: List of message dictionaries
            output_path: Path to save messages
        """
        import json

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

        logger.info(f"Messages saved to {output_path}")

    def format_for_display(self, messages: List[Dict[str, str]]) -> str:
        """
        Format messages for human-readable display.

        Args:
            messages: List of message dictionaries

        Returns:
            Formatted string
        """
        lines = []

        for i, msg in enumerate(messages):
            role = msg['role'].upper()
            content = msg['content']

            lines.append(f"{'='*70}")
            lines.append(f"MESSAGE {i+1}: {role}")
            lines.append(f"{'='*70}")
            lines.append(content)
            lines.append("")

        return "\n".join(lines)


class OpenAICompatiblePrompt:
    """Generate prompts compatible with OpenAI API calls."""

    def __init__(self):
        self.builder = PromptBuilder()

    def create_api_payload(self, target_skeleton: str,
                          examples: List[RetrievedExample],
                          model: str = "gpt-4",
                          temperature: float = 0.2,
                          max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Create complete API payload for OpenAI.

        Args:
            target_skeleton: Target skeleton to implement
            examples: Retrieved examples for few-shot
            model: OpenAI model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Complete API payload dictionary
        """
        messages = self.builder.build_messages(target_skeleton, examples)

        return {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

    def generate_with_openai(self, target_skeleton: str,
                           examples: List[RetrievedExample],
                           api_key: str = None,
                           **kwargs) -> str:
        """
        Generate code using OpenAI API.

        Args:
            target_skeleton: Target skeleton
            examples: Retrieved examples
            api_key: OpenAI API key
            **kwargs: Additional arguments for API call

        Returns:
            Generated code as string
        """
        try:
            import openai

            if api_key:
                openai.api_key = api_key

            payload = self.create_api_payload(target_skeleton, examples, **kwargs)

            response = openai.ChatCompletion.create(**payload)

            return response.choices[0].message.content

        except ImportError:
            logger.error("openai package not installed. Install with: pip install openai")
            return None
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return None


def main():
    """Test the prompt builder."""
    from rag_retriever import RetrievedExample

    # Create test examples
    examples = [
        RetrievedExample(
            class_name="Adder",
            skeleton="class Adder:\n    def add(self, a: int, b: int) -> int:\n        pass",
            implementation="class Adder:\n    def add(self, a: int, b: int) -> int:\n        return a + b",
            similarity_score=0.85,
            index=0,
            metadata={}
        ),
        RetrievedExample(
            class_name="Multiplier",
            skeleton="class Multiplier:\n    def multiply(self, a: int, b: int) -> int:\n        pass",
            implementation="class Multiplier:\n    def multiply(self, a: int, b: int) -> int:\n        return a * b",
            similarity_score=0.78,
            index=1
        )
    ]

    # Test prompt builder
    target = "class Calculator:\n    def calculate(self, x: int, y: int) -> int:\n        pass"

    builder = PromptBuilder()

    # Build messages
    messages = builder.build_messages(target, examples)

    print("="*70)
    print("GENERATED MESSAGES FOR OPENAI API")
    print("="*70)
    print(f"\nTotal messages: {len(messages)}")
    print(f"Few-shot examples: {len(examples)}")
    print()

    # Display formatted
    print(builder.format_for_display(messages))

    # Show as JSON
    import json
    print("\n" + "="*70)
    print("JSON FORMAT")
    print("="*70)
    print(json.dumps(messages, indent=2))


if __name__ == "__main__":
    main()