from typing import Dict, Iterator
import requests

class EnsemblBiomartHandler:
    """A class that handles Ensembl genes, transcripts and exons downloads via schug-web."""

    def __init__(self, build: str='37'):
        self.build: str = BUILDS[build]

    def stream_get(self, url: str) -> Iterator:
        """Sends a request to Schug web and returns the resource lines."""
        response: requests.models.responses = requests.get(url, stream=True)
        return response.iter_lines(decode_unicode=True)

    def stream_resource(self, interval_type: str) -> Iterator[str]:
        """Use schug web to fetch genes, transcripts or exons from a remote Ensembl biomart in the right genome build and save them to file."""
        shug_url: str = f'{SCHUG_BASE}{SCHUG_RESOURCE_URL[interval_type]}{self.build}'
        return self.stream_get(shug_url)