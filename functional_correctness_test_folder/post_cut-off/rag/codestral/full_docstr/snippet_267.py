
import os
import re
import numpy as np
from typing import List, Union
from misaki import Misaki
from misaki.utils import load_voice


class KokoroTTS:
    '''
    KokoroTTS class for text-to-speech generation using the Kokoro model.
    This class provides a simple interface for loading and using the Kokoro model
    to generate speech from text prompts.
    Example:
