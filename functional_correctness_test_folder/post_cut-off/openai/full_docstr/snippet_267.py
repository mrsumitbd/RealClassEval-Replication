
import os
import re
import numpy as np
import torch
import soundfile as sf

try:
    from kokoro import TTS
except ImportError as exc:
    raise ImportError(
        "The 'kokoro' package is required for KokoroTTS. "
        "Install it with: pip install kokoro"
    ) from exc


class KokoroTTS:
    '''
    KokoroTTS class for text-to-speech generation using the Kokoro model.
    This class provides a simple interface for loading and using the Kokoro model
    to generate speech from text prompts.
    Example:
