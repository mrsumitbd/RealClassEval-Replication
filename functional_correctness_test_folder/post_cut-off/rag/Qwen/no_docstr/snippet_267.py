
import numpy as np
import re
from pathlib import Path
import torch
from transformers import AutoModelForTextToSpeech, AutoProcessor


class KokoroTTS:
    '''
    KokoroTTS class for text-to-speech generation using the Kokoro model.
    This class provides a simple interface for loading and using the Kokoro model
    to generate speech from text prompts.
    Example:
