import httpx
import logging

class LLMClient:
    """Manages communication with the LLM provider."""

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key

    def get_response(self, messages: list[dict[str, str]]) -> str:
        """Get a response from the LLM.

        Args:
            messages: A list of message dictionaries.

        Returns:
            The LLM's response as a string.

        Raises:
            httpx.RequestError: If the request to the LLM fails.
        """
        url = 'https://api.groq.com/openai/v1/chat/completions'
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.api_key}'}
        payload = {'messages': messages, 'model': 'llama-3.2-90b-vision-preview', 'temperature': 0.7, 'max_tokens': 4096, 'top_p': 1, 'stream': False, 'stop': None}
        try:
            with httpx.Client() as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data['choices'][0]['message']['content']
        except httpx.RequestError as e:
            error_message = f'Error getting LLM response: {str(e)}'
            logging.error(error_message)
            if isinstance(e, httpx.HTTPStatusError):
                status_code = e.response.status_code
                logging.error(f'Status code: {status_code}')
                logging.error(f'Response details: {e.response.text}')
            return f'I encountered an error: {error_message}. Please try again or rephrase your request.'