
import os
import re
import numpy as np
import torch
import soundfile as sf

try:
    from kokoro.tts import TTS
except Exception as exc:
    raise ImportError(
        "kokoro.tts module not found. Install the 'kokoro' package.") from exc


class KokoroTTS:
    '''
    KokoroTTS class for text-to-speech generation using the Kokoro model.
    This class provides a simple interface for loading and using the Kokoro model
    to generate speech from text prompts.
    Example:
