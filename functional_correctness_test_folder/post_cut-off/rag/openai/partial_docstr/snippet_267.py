
import os
import re
from pathlib import Path
from typing import List

import numpy as np

# Import the TTS engine from misaki (Kokoro is a wrapper around it)
try:
    from misaki import TTS
except Exception as exc:  # pragma: no cover
    raise ImportError(
        "The `misaki` package is required for KokoroTTS. "
        "Install it with `pip install misaki`."
    ) from exc

# Import soundfile for writing wav files
try:
    import soundfile as sf
except Exception as exc:  # pragma: no cover
    raise ImportError(
        "The `soundfile` package is required for KokoroTTS. "
        "Install it with `pip install soundfile`."
    ) from exc


class KokoroTTS:
    """
    KokoroTTS class for text-to-speech generation using the Kokoro model.
    This class provides a simple interface for loading and using the Kokoro model
    to generate speech from text prompts.
    """

    # Mapping from the single‑letter language codes used by Kokoro to the
    # language identifiers understood by misaki.
    _LANG
