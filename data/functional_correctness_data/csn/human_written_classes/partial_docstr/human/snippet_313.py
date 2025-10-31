class EnThTranslator:
    """
    English-Thai Machine Translation

    from VISTEC-depa Thailand Artificial Intelligence Research Institute

    Website: https://airesearch.in.th/releases/machine-translation-models/

    :param bool use_gpu : load model using GPU (Default is False)
    """

    def __init__(self, use_gpu: bool=False):
        self._tokenizer = MosesTokenizer('en')
        self._model_name = _EN_TH_MODEL_NAME
        _download_install(self._model_name)
        self._model = TransformerModel.from_pretrained(model_name_or_path=_get_translate_path(self._model_name, _EN_TH_FILE_NAME, 'models'), checkpoint_file='checkpoint.pt', data_name_or_path=_get_translate_path(self._model_name, _EN_TH_FILE_NAME, 'vocab'))
        if use_gpu:
            self._model = self._model.cuda()

    def translate(self, text: str) -> str:
        """
        Translate text from English to Thai

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from English to Thai::

            from pythainlp.translate import EnThTranslator

            enth = EnThTranslator()

            enth.translate("I love cat.")
            # output: ฉันรักแมว

        """
        tokens = ' '.join(self._tokenizer.tokenize(text))
        translated = self._model.translate(tokens)
        return translated.replace(' ', '').replace('▁', ' ').strip()