import os
import mistralai
import time, json
import logging
from pathlib import Path
import backoff
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import List
from dotenv import load_dotenv
load_dotenv('../.env')

def generate_with_mistral(skeletons, model):

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)

    # Validate inputs
    if not skeletons:
        logger.error("No skeletons provided")
        raise ValueError("Skeletons list cannot be empty")
    for i, skeleton in enumerate(skeletons):
        if not isinstance(skeleton, str) or not skeleton.strip():
            logger.error(f"Invalid skeleton at index {i}: must be a non-empty string")
            raise ValueError(f"Invalid skeleton at index {i}")
    
    client = mistralai.Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    generated_snippets = []

    counter = 1
    for skeleton in skeletons:
        if not isinstance(skeleton, str) or not skeleton.strip():
            raise ValueError("Each skeleton must be a non-empty string")
        
        else:
            response = client.chat.complete(
                model=model,
                temperature=0.0,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python programmer who can correctly implement complete Python classes based on the provided class skeleton."
                    },
                    {
                        "role": "user",
                        "content": f"Implement the following class. Do not explain the code. The given class skeleton is as follows:\n{skeleton}"
                    }
                ]
            )
            code_snippet = response.choices[0].message.content

            generated_snippets.append(code_snippet)
            logger.info(f"Generated snippet {counter}/{len(skeletons)}")
            counter += 1
            time.sleep(1)  # To respect rate limits
    
    return generated_snippets


def few_shot_generation_with_mistral(
        snippet_ids: List[str],
        model: str,
        prompt_location: str = None,
        timeout: int = 20  # Timeout in seconds
) -> List[str]:
    """Generate code using Mistral API with few-shot prompts."""

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger(__name__)

    # Validate inputs
    if not snippet_ids:
        raise ValueError("snippet_ids cannot be empty")

    if not prompt_location:
        raise ValueError("prompt_location must be specified")

    prompt_dir = Path(prompt_location)
    if not prompt_dir.exists():
        raise ValueError(f"Prompt directory does not exist: {prompt_location}")

    # Initialize client
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set")

    import mistralai
    client = mistralai.Mistral(api_key=api_key)

    # Add exponential backoff - catch generic exceptions
    @backoff.on_exception(
        backoff.expo,
        (Exception,),  # Catch all exceptions
        max_tries=3,
        giveup=lambda e: 'rate limit' not in str(e).lower()  # Only retry on rate limit
    )
    def api_call_with_backoff(messages):
        return client.chat.complete(
            model=model,
            temperature=0.0,
            messages=messages
        )

    def api_call_with_timeout(messages, timeout_seconds):
        """Execute API call with timeout using ThreadPoolExecutor."""
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(api_call_with_backoff, messages)
            try:
                response = future.result(timeout=timeout_seconds)
                return response
            except FuturesTimeoutError:
                logger.warning(f"API call timed out after {timeout_seconds} seconds")
                return None
            except Exception as e:
                logger.error(f"API call failed: {e}")
                return None

    generated_snippets = []

    for i, snippet in enumerate(snippet_ids, start=1):
        prompt_file = prompt_dir / f"prompt_{snippet}.json"

        if not prompt_file.exists():
            logger.error(f"Prompt file not found: {prompt_file}")
            generated_snippets.append(None)  # Maintain alignment
            continue

        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)

            # Call API with timeout
            logger.info(f"[{i}/{len(snippet_ids)}] Calling API for: {snippet}")
            response = api_call_with_timeout(messages, timeout)

            if response is None:
                logger.error(f"[{i}/{len(snippet_ids)}] Timeout/Error for {snippet} - skipping")
                generated_snippets.append(None)
                continue

            code_snippet = response.choices[0].message.content
            generated_snippets.append(code_snippet)

            logger.info(f"[{i}/{len(snippet_ids)}] Generated: {snippet}")

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {prompt_file}: {e}")
            generated_snippets.append(None)
            continue
        except Exception as e:
            logger.error(f"Error generating {snippet}: {e}")
            generated_snippets.append(None)
            # Don't raise - continue with other snippets

    success_count = sum(1 for s in generated_snippets if s is not None)
    logger.info(f"Successfully generated {success_count}/{len(snippet_ids)} snippets")
    return generated_snippets
