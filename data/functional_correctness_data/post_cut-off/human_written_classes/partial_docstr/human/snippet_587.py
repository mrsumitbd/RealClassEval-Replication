from typing import Dict, List
from dashscope.api_entities.dashscope_response import SpeechSynthesisResponse

class SpeechSynthesisResult:
    """The result set of speech synthesis, including audio data,
       timestamp information, and final result information.
    """
    _audio_frame: bytes = None
    _audio_data: bytes = None
    _sentence: Dict[str, str] = None
    _sentences: List[Dict[str, str]] = None
    _response: SpeechSynthesisResponse = None

    def __init__(self, frame: bytes, data: bytes, sentence: Dict[str, str], sentences: List[Dict[str, str]], response: SpeechSynthesisResponse):
        if frame is not None:
            self._audio_frame = bytes(frame)
        if data is not None:
            self._audio_data = bytes(data)
        if sentence is not None:
            self._sentence = sentence
        if sentences is not None:
            self._sentences = sentences
        if response is not None:
            self._response = response

    def get_audio_frame(self) -> bytes:
        """Obtain the audio frame data of speech synthesis through callbacks.
        """
        return self._audio_frame

    def get_audio_data(self) -> bytes:
        """Get complete audio data for speech synthesis.
        """
        return self._audio_data

    def get_timestamp(self) -> Dict[str, str]:
        """Obtain the timestamp information of the current speech synthesis
        sentence through the callback.
        """
        return self._sentence

    def get_timestamps(self) -> List[Dict[str, str]]:
        """Get complete timestamp information for all speech synthesis sentences.
        """
        return self._sentences

    def get_response(self) -> SpeechSynthesisResponse:
        """Obtain the status information of the current speech synthesis task,
        including error information and billing information.
        """
        return self._response