from onnxruntime import InferenceSession
import json
import numpy as np
from pythainlp.corpus import get_corpus_path

class ThaiTransliterator_ONNX:

    def __init__(self):
        """
        Transliteration of Thai words.

        Now supports Thai to Latin (romanization)
        """
        self.__encoder_filename = get_corpus_path(_MODEL_ENCODER_NAME)
        self.__decoder_filename = get_corpus_path(_MODEL_DECODER_NAME)
        self.__config_filename = get_corpus_path(_MODEL_CONFIG_NAME)
        with open(str(self.__config_filename)) as f:
            loader = json.load(f)
        OUTPUT_DIM = loader['output_dim']
        self._maxlength = 100
        self._char_to_ix = loader['char_to_ix']
        self._ix_to_char = loader['ix_to_char']
        self._target_char_to_ix = loader['target_char_to_ix']
        self._ix_to_target_char = loader['ix_to_target_char']
        self._encoder = InferenceSession(self.__encoder_filename)
        self._decoder = InferenceSession(self.__decoder_filename)
        self._network = Seq2Seq_ONNX(self._encoder, self._decoder, self._target_char_to_ix['<start>'], self._target_char_to_ix['<end>'], self._maxlength, target_vocab_size=OUTPUT_DIM)

    def _prepare_sequence_in(self, text: str):
        """
        Prepare input sequence for ONNX
        """
        idxs = []
        for ch in text:
            if ch in self._char_to_ix:
                idxs.append(self._char_to_ix[ch])
            else:
                idxs.append(self._char_to_ix['<UNK>'])
        idxs.append(self._char_to_ix['<end>'])
        return np.array(idxs)

    def romanize(self, text: str) -> str:
        """
        :param str text: Thai text to be romanized
        :return: English (more or less) text that spells out how the Thai text
                 should be pronounced.
        """
        input_tensor = self._prepare_sequence_in(text).reshape(1, -1)
        input_length = [len(text) + 1]
        target_tensor_logits = self._network.run(input_tensor, input_length)
        if target_tensor_logits.shape[0] == 0:
            target = ['<PAD>']
        else:
            target_tensor = np.argmax(target_tensor_logits.squeeze(1), 1)
            target = [self._ix_to_target_char[str(t)] for t in target_tensor]
        return ''.join(target)