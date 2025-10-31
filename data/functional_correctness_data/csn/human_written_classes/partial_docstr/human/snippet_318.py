import torch
import torch.nn.functional as F
from pythainlp.corpus import get_corpus_path

class ThaiTransliterator:

    def __init__(self):
        """
        Transliteration of Thai words.

        Now supports Thai to Latin (romanization)
        """
        self.__model_filename = get_corpus_path(_MODEL_NAME)
        loader = torch.load(self.__model_filename, map_location=device)
        INPUT_DIM, E_EMB_DIM, E_HID_DIM, E_DROPOUT = loader['encoder_params']
        OUTPUT_DIM, D_EMB_DIM, D_HID_DIM, D_DROPOUT = loader['decoder_params']
        self._maxlength = 100
        self._char_to_ix = loader['char_to_ix']
        self._ix_to_char = loader['ix_to_char']
        self._target_char_to_ix = loader['target_char_to_ix']
        self._ix_to_target_char = loader['ix_to_target_char']
        self._encoder = Encoder(INPUT_DIM, E_EMB_DIM, E_HID_DIM, E_DROPOUT)
        self._decoder = AttentionDecoder(OUTPUT_DIM, D_EMB_DIM, D_HID_DIM, D_DROPOUT)
        self._network = Seq2Seq(self._encoder, self._decoder, self._target_char_to_ix['<start>'], self._target_char_to_ix['<end>'], self._maxlength).to(device)
        self._network.load_state_dict(loader['model_state_dict'])
        self._network.eval()

    def _prepare_sequence_in(self, text: str):
        """
        Prepare input sequence for PyTorch
        """
        idxs = []
        for ch in text:
            if ch in self._char_to_ix:
                idxs.append(self._char_to_ix[ch])
            else:
                idxs.append(self._char_to_ix['<UNK>'])
        idxs.append(self._char_to_ix['<end>'])
        tensor = torch.tensor(idxs, dtype=torch.long)
        return tensor.to(device)

    def romanize(self, text: str) -> str:
        """
        :param str text: Thai text to be romanized
        :return: English (more or less) text that spells out how the Thai text
                 should be pronounced.
        """
        input_tensor = self._prepare_sequence_in(text).view(1, -1)
        input_length = torch.Tensor([len(text) + 1]).int()
        target_tensor_logits = self._network(input_tensor, input_length, None, 0)
        if target_tensor_logits.size(0) == 0:
            target = ['<PAD>']
        else:
            target_tensor = torch.argmax(target_tensor_logits.squeeze(1), 1).cpu().detach().numpy()
            target = [self._ix_to_target_char[t] for t in target_tensor]
        return ''.join(target)