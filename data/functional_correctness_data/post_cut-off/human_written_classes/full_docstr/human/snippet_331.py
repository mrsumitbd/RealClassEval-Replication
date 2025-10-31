from air.models import AsyncModelsClient, ModelsClient
from air.embeddings import AsyncEmbeddingsClient, EmbeddingsClient
from air.images import AsyncImagesClient, ImagesClient
from air.distiller import AsyncDistillerClient
from air.knowledge import AsyncKnowledgeClient, KnowledgeClient
from air.chat import AsyncChatClient, ChatClient
from air.audio import AsyncAudio, Audio

class AsyncAIRefinery:
    """
    A top-level client that exposes various sub-clients in a single interface,
    operating asynchronously.

    Example usage:

        client = AsyncAIRefinery(
            api_key="...",
            base_url="...",
            default_headers={"X-Client-Version": "1.2.3"}
        )

        # Use chat
        response = await client.chat.completions.create(
            model="model-name", messages=[...]
        )

        # Use embeddings
        embeddings_response = await client.embeddings.create(
            model="model-name", input=["Hello"]
        )

        # Use tts
        tts_response = await client.audio.speech.create(
            model="model-name",
            input="Hello, this is a test of text-to-speech synthesis.",
            voice="en-US-JennyNeural",
            response_format="mp3",  # Optional
            speed=1.0  # Optional

        # Use asr
        asr_response = await client.audio.transcriptions.create(
            model="model-name",
            file=file
        )

        # Use models
        models_list = await client.models.list()

        # Use distiller
        async with client.distiller(project="...", uuid="...") as dc:
            responses = await dc.query(query="hi")
            async for response in responses:
                print(response)

        # Use images
        embeddings_response = await client.images.generate(
            prompt="A cute baby sea otter", model="model-name"
        )

        # Use knowledge
        graph_client = client.graph
        graph_client.create_project(graph_config=...)
        status = await graph_client.build(files_path=..)
    """

    def __init__(self, api_key: str, base_url: str='https://api.airefinery.accenture.com', default_headers: dict[str, str] | None=None, **kwargs):
        """
        Initializes the asynchronous unified client with sub-clients.

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
        self.chat = AsyncChatClient(base_url=self._update_inference_endpoint(), api_key=self.api_key, default_headers=self.default_headers)
        self.embeddings = AsyncEmbeddingsClient(base_url=self._update_inference_endpoint(), api_key=self.api_key, default_headers=self.default_headers)
        self.audio = AsyncAudio(base_url=self._update_inference_endpoint(), api_key=self.api_key, default_headers=self.default_headers)
        self.models = AsyncModelsClient(base_url=self._update_inference_endpoint(), api_key=self.api_key, default_headers=self.default_headers)
        self.distiller = AsyncDistillerClient(base_url=self.base_url, api_key=self.api_key, default_headers=self.default_headers)
        self.images = AsyncImagesClient(base_url=self._update_inference_endpoint(), api_key=self.api_key, default_headers=self.default_headers)
        self.knowledge = AsyncKnowledgeClient(base_url=self.base_url, api_key=self.api_key, default_headers=self.default_headers)

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