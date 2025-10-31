class ThEnTranslator:
    """
    Thai-English Machine Translation

    from VISTEC-depa Thailand Artificial Intelligence Research Institute

    Website: https://airesearch.in.th/releases/machine-translation-models/

    :param bool use_gpu : load model using GPU (Default is False)
    """

    def __init__(self, use_gpu: bool=False):
        self._model_name = _TH_EN_MODEL_NAME
        _download_install(self._model_name)
        self._model = TransformerModel.from_pretrained(model_name_or_path=_get_translate_path(self._model_name, _TH_EN_FILE_NAME, 'models'), checkpoint_file='checkpoint.pt', data_name_or_path=_get_translate_path(self._model_name, _TH_EN_FILE_NAME, 'vocab'), bpe='sentencepiece', sentencepiece_model=_get_translate_path(self._model_name, _TH_EN_FILE_NAME, 'bpe', 'spm.th.model'))
        if use_gpu:
            self._model.cuda()

    def translate(self, text: str) -> str:
        """
        Translate text from Thai to English

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Thai to English::

            from pythainlp.translate import ThEnTranslator

            then = ThEnTranslator()

            then.translate("ฉันรักแมว")
            # output: I love cat.

        """
        return self._model.translate(text)