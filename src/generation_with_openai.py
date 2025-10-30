import os
from pyexpat.errors import messages

import openai
import json
import time
from pathlib import Path
import backoff
import logging
from typing import List, Optional
from dotenv import load_dotenv
load_dotenv('../.env')


def batch_generate_with_openai(
    skeletons: List[str],
    model: str,
    temperature: float = 0.0,
    reasoning_effort: Optional[str] = None,  # Ignored for Codex
    max_tokens: int = 8192  # Added for Codex
) -> List[str]:
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Exponential backoff decorator
    @backoff.on_exception(backoff.expo, openai.RateLimitError)
    def api_call_with_backoff(fn, *args, **kwargs):
        return fn(*args, **kwargs)

    def is_reasoning_model(model: str) -> bool:
        """Test if the model is a reasoning model or Codex by checking if 'temperature' causes an error."""
        try:
            api_call_with_backoff(
                client.chat.completions.create,
                model=model,
                messages=[{"role": "user", "content": "test"}],
                temperature=0.7,
                max_tokens=1
            )
            return False
        except openai.BadRequestError as e:
            error_msg = str(e).lower()
            if "temperature" in error_msg or "unsupported" in error_msg:
                return True
            raise  # Re-raise if different error

    def is_codex_model(model: str) -> bool:
        """Check if the model is a Codex model (e.g., contains 'codex')."""
        return "codex" in model.lower()

    # Detect model type
    use_codex = is_codex_model(model)
    use_reasoning = is_reasoning_model(model) if not use_codex else True  # Codex behaves like reasoning (no temperature)
    logger.info(f"Model {model} detected as {'Codex' if use_codex else 'reasoning' if use_reasoning else 'non-reasoning'} model")

    # System prompt
    system_prompt = (
        "You are an expert Python programmer who can correctly implement complete Python classes "
        "based on the provided class skeleton."
    )

    # Create batch requests JSONL
    file_path = 'batch_requests.jsonl'
    with open(file_path, 'w') as f:
        for i, skeleton in enumerate(skeletons):
            user_prompt = f"Implement the following class. Do not explain the code. The given class skeleton is as follows:\n{skeleton}"
            if use_codex:
                # Codex uses /v1/responses with a single prompt
                body = {
                    "model": model,
                    "prompt": f"{system_prompt}\n{user_prompt}",
                    "max_tokens": max_tokens
                }
            else:
                # Non-Codex models use chat completions
                if use_reasoning:
                    messages = [
                        {"role": "developer", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                else:
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                body = {
                    "model": model,
                    "messages": messages
                }
                if not use_reasoning:
                    body["temperature"] = temperature
                if use_reasoning and reasoning_effort and not use_codex:
                    body["reasoning_effort"] = reasoning_effort

            request = {
                "custom_id": f"request-{i}",
                "method": "POST",
                "url": "/v1/responses" if use_codex else "/v1/chat/completions",
                "body": body
            }
            f.write(json.dumps(request) + '\n')
    logger.info(f"Created batch file {file_path} with {len(skeletons)} requests")

    # Upload file
    with open(file_path, 'rb') as f:
        file_response = api_call_with_backoff(client.files.create, file=f, purpose='batch')
    file_id = file_response.id
    logger.info(f"Uploaded batch file, ID: {file_id}")

    # Create batch job
    batch = api_call_with_backoff(
        client.batches.create,
        input_file_id=file_id,
        endpoint="/v1/responses" if use_codex else "/v1/chat/completions",
        completion_window="24h"
    )
    batch_id = batch.id
    logger.info(f"Created batch job, ID: {batch_id}")

    # Poll for completion
    while True:
        status = api_call_with_backoff(client.batches.retrieve, batch_id)
        completed = 0
        total = len(skeletons)
        if hasattr(status, 'request_counts'):
            completed = status.request_counts.completed
            total = status.request_counts.total
        logger.info(f"Polling batch job {batch_id}: Status: {status.status}, Requests processed: {completed}/{total}")
        if status.status == 'completed':
            output_file_id = status.output_file_id
            logger.info(f"Batch completed, output file ID: {output_file_id}")
            error_file_id = status.error_file_id if hasattr(status, 'error_file_id') and status.error_file_id else None
            logger.info(f"Error file ID: {error_file_id if error_file_id else 'None'}")
            break
        elif status.status in ['failed', 'expired', 'cancelled']:
            logger.error(f"Batch failed with status: {status.status}")
            raise ValueError(f"Batch failed with status: {status.status}")
        time.sleep(30)  # Poll every 30 seconds

    # Retrieve output
    output_response = api_call_with_backoff(client.files.content, output_file_id)
    output_file_path = 'batch_outputs.jsonl'
    with open(output_file_path, 'wb') as f:
        f.write(output_response.content)
    logger.info(f"Downloaded batch output to {output_file_path}")

    # Retrieve error file if it exists
    error_file_path = None
    if error_file_id:
        error_response = api_call_with_backoff(client.files.content, error_file_id)
        error_file_path = 'batch_errors.jsonl'
        with open(error_file_path, 'wb') as f:
            f.write(error_response.content)
        logger.info(f"Downloaded error file to {error_file_path}")

    # Extract code snippets
    results = {}
    with open(output_file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            custom_id = data['custom_id']
            if data['response']['status_code'] == 200:
                if use_codex:
                    content = data['response']['body']['output']['text']
                else:
                    content = data['response']['body']['choices'][0]['message']['content']
                results[custom_id] = content
            else:
                results[custom_id] = None
                logger.warning(f"Request {custom_id} failed with status {data['response']['status_code']}")

    # Process error file if exists
    if error_file_path:
        with open(error_file_path, 'r') as f:
            for line in f:
                data = json.loads(line)
                custom_id = data['custom_id']
                results[custom_id] = None
                logger.warning(f"Request {custom_id} failed with error: {data.get('error', 'No error details')}")

    # Build code_snippets list in order
    code_snippets = []
    for i in range(len(skeletons)):
        custom_id = f"request-{i}"
        code_snippets.append(results.get(custom_id, None))

    logger.info(f"Extracted {len(code_snippets)} code snippets from batch output (including Nones for failures)")

    # Clean up files (optional)
    os.remove(file_path)
    os.remove(output_file_path)
    if error_file_path:
        os.remove(error_file_path)
    logger.info(f"Cleaned up temporary files")

    return code_snippets


def batch_few_shot_generation_with_openai(
        snippet_ids: List[str],
        model: str,
        prompt_location: str,
        temperature: float = 0.0,
        reasoning_effort: Optional[str] = None,
        max_tokens: int = 8192
) -> List[str]:
    """
    Generate code using OpenAI Batch API with few-shot prompts.

    Args:
        snippet_ids: List of snippet identifiers (e.g., ["snippet_351", "snippet_352"])
        model: OpenAI model name
        prompt_location: Directory containing prompt JSON files
        temperature: Temperature for non-reasoning models
        reasoning_effort: Reasoning effort for reasoning models
        max_tokens: Max tokens for completion

    Returns:
        List of generated code snippets (None for failures)
    """
    # Set up logging
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

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Exponential backoff decorator
    @backoff.on_exception(backoff.expo, openai.RateLimitError)
    def api_call_with_backoff(fn, *args, **kwargs):
        return fn(*args, **kwargs)

    def is_reasoning_model(model: str) -> bool:
        """Test if the model is a reasoning model by checking if 'temperature' causes an error."""
        try:
            api_call_with_backoff(
                client.chat.completions.create,
                model=model,
                messages=[{"role": "user", "content": "test"}],
                temperature=0.7,
                max_tokens=1
            )
            return False
        except openai.BadRequestError as e:
            error_msg = str(e).lower()
            if "temperature" in error_msg or "unsupported" in error_msg:
                return True
            raise

    def is_codex_model(model: str) -> bool:
        """Check if the model is a Codex model."""
        return "codex" in model.lower()

    # Detect model type
    use_codex = is_codex_model(model)
    use_reasoning = is_reasoning_model(model) if not use_codex else True
    logger.info(
        f"Model {model} detected as {'Codex' if use_codex else 'reasoning' if use_reasoning else 'non-reasoning'} model")

    # Create batch requests JSONL
    file_path = 'batch_requests.jsonl'
    with open(file_path, 'w') as f:
        for i, snippet_id in enumerate(snippet_ids):
            # Load the few-shot prompt from file
            prompt_file = prompt_dir / f"prompt_{snippet_id}.json"

            if not prompt_file.exists():
                logger.error(f"Prompt file not found: {prompt_file}")
                raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

            with open(prompt_file, 'r', encoding='utf-8') as pf:
                messages = json.load(pf)

            # Transform messages based on model type
            if use_codex:
                # Codex uses a single prompt string
                # Combine all messages into one prompt
                prompt_text = "\n\n".join([msg['content'] for msg in messages])
                body = {
                    "model": model,
                    "prompt": prompt_text,
                    "max_tokens": max_tokens
                }
            else:
                # For reasoning models, change "assistant" role to "developer"
                if use_reasoning:
                    transformed_messages = []
                    for msg in messages:
                        if msg['role'] == 'assistant':
                            transformed_messages.append({
                                'role': 'developer',
                                'content': msg['content']
                            })
                        else:
                            transformed_messages.append(msg)
                    messages = transformed_messages

                # Build body for chat completions
                body = {
                    "model": model,
                    "messages": messages
                }

                # Add temperature for non-reasoning models
                if not use_reasoning:
                    body["temperature"] = temperature

                # Add reasoning effort for reasoning models
                if use_reasoning and reasoning_effort:
                    body["reasoning_effort"] = reasoning_effort

            # Create batch request
            request = {
                "custom_id": f"{snippet_id}",  # Use snippet_id as custom_id
                "method": "POST",
                "url": "/v1/responses" if use_codex else "/v1/chat/completions",
                "body": body
            }
            f.write(json.dumps(request) + '\n')

    logger.info(f"Created batch file {file_path} with {len(snippet_ids)} requests")

    # Upload file
    with open(file_path, 'rb') as f:
        file_response = api_call_with_backoff(client.files.create, file=f, purpose='batch')
    file_id = file_response.id
    logger.info(f"Uploaded batch file, ID: {file_id}")

    # Create batch job
    batch = api_call_with_backoff(
        client.batches.create,
        input_file_id=file_id,
        endpoint="/v1/responses" if use_codex else "/v1/chat/completions",
        completion_window="24h"
    )
    batch_id = batch.id
    logger.info(f"Created batch job, ID: {batch_id}")

    # Poll for completion
    while True:
        status = api_call_with_backoff(client.batches.retrieve, batch_id)
        completed = 0
        total = len(snippet_ids)
        if hasattr(status, 'request_counts'):
            completed = status.request_counts.completed
            total = status.request_counts.total
        logger.info(f"Polling batch {batch_id}: Status: {status.status}, Progress: {completed}/{total}")

        if status.status == 'completed':
            output_file_id = status.output_file_id
            logger.info(f"Batch completed! Output file ID: {output_file_id}")
            error_file_id = status.error_file_id if hasattr(status, 'error_file_id') and status.error_file_id else None
            if error_file_id:
                logger.warning(f"Error file ID: {error_file_id}")
            break
        elif status.status in ['failed', 'expired', 'cancelled']:
            logger.error(f"Batch failed with status: {status.status}")
            raise ValueError(f"Batch failed with status: {status.status}")

        time.sleep(30)  # Poll every 30 seconds

    # Retrieve output
    output_response = api_call_with_backoff(client.files.content, output_file_id)
    output_file_path = 'batch_outputs.jsonl'
    with open(output_file_path, 'wb') as f:
        f.write(output_response.content)
    logger.info(f"Downloaded batch output to {output_file_path}")

    # Retrieve error file if it exists
    error_file_path = None
    if error_file_id:
        error_response = api_call_with_backoff(client.files.content, error_file_id)
        error_file_path = 'batch_errors.jsonl'
        with open(error_file_path, 'wb') as f:
            f.write(error_response.content)
        logger.warning(f"Downloaded error file to {error_file_path}")

    # Extract code snippets
    results = {}
    with open(output_file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            custom_id = data['custom_id']
            if data['response']['status_code'] == 200:
                if use_codex:
                    content = data['response']['body']['output']['text']
                else:
                    content = data['response']['body']['choices'][0]['message']['content']
                results[custom_id] = content
            else:
                results[custom_id] = None
                logger.warning(f"Request {custom_id} failed with status {data['response']['status_code']}")

    # Process error file if exists
    if error_file_path:
        with open(error_file_path, 'r') as f:
            for line in f:
                data = json.loads(line)
                custom_id = data['custom_id']
                error_msg = data.get('error', {})
                results[custom_id] = None
                logger.warning(f"Request {custom_id} failed: {error_msg}")

    # Build code_snippets list in order of snippet_ids
    code_snippets = []
    for snippet_id in snippet_ids:
        code_snippets.append(results.get(snippet_id, None))

    success_count = sum(1 for c in code_snippets if c is not None)
    logger.info(f"✓ Successfully generated {success_count}/{len(snippet_ids)} code snippets")

    # Clean up files (optional)
    try:
        os.remove(file_path)
        os.remove(output_file_path)
        if error_file_path and os.path.exists(error_file_path):
            os.remove(error_file_path)
        logger.info(f"Cleaned up temporary files")
    except Exception as e:
        logger.warning(f"Could not clean up temporary files: {e}")

    return code_snippets

def generate_with_openai(skeletons, model):

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
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    generated_snippets = []

    # defining exponential backoff
    @backoff.on_exception(backoff.expo, openai.RateLimitError)
    def completions_with_backoff(**kwargs):
        return client.chat.completions.create(**kwargs)

    counter = 1
    for skeleton in skeletons:
        if not isinstance(skeleton, str) or not skeleton.strip():
            raise ValueError("Each skeleton must be a non-empty string")
        
        else:
            response = completions_with_backoff(
                model=model,
                # reasoning={"effort": "low"},
                temperature=0.0,
                messages=[
                    {
                        "role": "developer",
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
    
    return generated_snippets


def few_shot_generation_with_openai(
        snippet_ids: List[str],
        model: str,
        reasoning: bool = False,
        prompt_location: str = None
) -> List[str]:
    """Generate code using OpenAI API with few-shot prompts."""

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
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = openai.OpenAI(api_key=api_key)

    @backoff.on_exception(backoff.expo, openai.RateLimitError)
    def completions_with_backoff(**kwargs):
        return client.chat.completions.create(**kwargs)

    generated_snippets = []

    for i, snippet in enumerate(snippet_ids, start=1):
        # Validate snippet format
        if "snippet" not in snippet:
            logger.warning(f"Unusual snippet name at index {i}: {snippet}")

        prompt_file = prompt_dir / f"prompt_{snippet}.json"

        if not prompt_file.exists():
            logger.error(f"Prompt file not found: {prompt_file}")
            continue  # Skip instead of crashing (or use 'raise' if you prefer)

        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)

            response = completions_with_backoff(
                model=model,
                messages=messages,
                **({"reasoning": {"effort": "low"}} if reasoning else {"temperature": 0.0})
            )

            code_snippet = response.choices[0].message.content
            generated_snippets.append(code_snippet)

            logger.info(f"[{i}/{len(snippet_ids)}] Generated: {snippet}")

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {prompt_file}: {e}")
            continue
        except Exception as e:
            logger.error(f"Error generating {snippet}: {e}")
            raise

    logger.info(f"Successfully generated {len(generated_snippets)}/{len(snippet_ids)} snippets")
    return generated_snippets
