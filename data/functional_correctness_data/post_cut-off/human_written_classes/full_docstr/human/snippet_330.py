from air.knowledge import AsyncKnowledgeClient, KnowledgeClient
from air.chat import AsyncChatClient, ChatClient
from air.embeddings import AsyncEmbeddingsClient, EmbeddingsClient
from air.models import AsyncModelsClient, ModelsClient
from air.audio import AsyncAudio, Audio
from air.images import AsyncImagesClient, ImagesClient

class AIRefinery:
    """
    A top-level client that exposes various sub-clients in a single interface,
    operating synchronously.

    Example usage:

        client = AIRefinery(
            api_key="...",
            base_url="...",
            default_headers={"X-Client-Version": "1.2.3"}
        )

        # Use chat
        response = client.chat.completions.create(
            model="model-name", messages=[...]
        )

        # Use embeddings
        embeddings_response = client.embeddings.create(
            model="model-name", input=["Hello"]
        )

        # Use tts
        tts_response = client.audio.speech.create(
            model="model-name",
            input="Hello, this is a test of text-to-speech synthesis.",
            voice="en-US-JennyNeural",
            response_format="mp3",  # Optional
            speed=1.0  # Optional

        # Use asr
        asr_response = client.speech_to_text.create(
            model="model-name",
            file=["audio1.wav", "audio2.wav"]
        )

        # Use models
        models_list = client.models.list()

        # Use images
        image_response = await client.images.generate(
            prompt="A cute baby sea otter", model="model-name"
        )

        # Use knowledge
        knowledge_client = client.knowledge
        knowledge_client.create_project(config)
        knowledge_response = await knowledge_client.document_processing.parse_documents(file_path='', model='')

        # Attempting to use client.distiller will raise an exception
        # (not supported in sync mode).
    """

    def __init__(self, api_key: str, base_url: str='https://api.airefinery.accenture.com', default_headers: dict[str, str] | None=None, **kwargs):
        """
        Initializes the synchronous unified client with sub-clients.

        Args:

            api_key (str): Your API key or token for authenticated requests.
            base_url (str, optional): Base URL for your API endpoints.
                Defaults to "https://api.airefinery.accenture.com".
            default_headers (dict[str, str] | None): Headers that apply to
                every request made by sub-clients (e.g., {"X-Client-Version": "1.2.3"}).
            **kwargs: Additional configuration parameters, if any.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.default_headers = default_headers or {}
        self.kwargs = kwargs
        self.chat = ChatClient(base_url=self._update_inference_endpoint(), api_key=self.api_key, default_headers=self.default_headers)
        self.embeddings = EmbeddingsClient(base_url=self._update_inference_endpoint(), api_key=self.api_key, default_headers=self.default_headers)
        self.audio = Audio(base_url=self._update_inference_endpoint(), api_key=self.api_key, default_headers=self.default_headers)
        self.models = ModelsClient(base_url=self._update_inference_endpoint(), api_key=self.api_key, default_headers=self.default_headers)
        self.images = ImagesClient(base_url=self._update_inference_endpoint(), api_key=self.api_key, default_headers=self.default_headers)
        self.knowledge = KnowledgeClient(base_url=self.base_url, api_key=self.api_key, default_headers=self.default_headers)

    def _update_inference_endpoint(self):
        """
        Ensures the base_url ends with the '/inference' suffix if necessary.

        This method checks whether the `base_url` ends with "/inference".
        If it does not, the method appends "/inference" to the URL and returns
        the updated URL. This is particularly useful for ensuring compatibility
        with authentication mechanisms like auth.openai(), where the "/inference"
        suffix is automatically appended to the base URL.

        Returns:
            str: The base URL with "/inference" appended if it was not already present.
        """
        if not self.base_url.endswith('/inference'):
            return self.base_url.rstrip('/') + '/inference'
        return self.base_url

    @property
    def distiller(self):
        """
        Distiller is only supported in the asynchronous client.
        Accessing this property in the synchronous client will raise a NotImplementedError.
        """
        raise NotImplementedError('Distiller is only available in async mode. Please use AsyncAIRefinery instead.')