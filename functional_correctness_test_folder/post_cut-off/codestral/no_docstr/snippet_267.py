
import os
import re
import torch
import torchaudio
from transformers import AutoModelForTextToSpectrogram, AutoProcessor


class KokoroTTS:
    '''
    KokoroTTS class for text-to-speech generation using the Kokoro model.
    This class provides a simple interface for loading and using the Kokoro model
    to generate speech from text prompts.
    Example:
