class ThZhTranslator:
    """
    Thai-Chinese Machine Translation

    from Lalita @ AI builder

    - GitHub: https://github.com/LalitaDeelert/lalita-mt-zhth
    - Facebook post https://web.facebook.com/aibuildersx/posts/166736255494822

    :param bool use_gpu : load model using GPU (Default is False)
    """

    def __init__(self, use_gpu: bool=False, pretrained: str='Lalita/marianmt-th-zh_cn') -> None:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        self.tokenizer_thzh = AutoTokenizer.from_pretrained(pretrained)
        self.model_thzh = AutoModelForSeq2SeqLM.from_pretrained(pretrained)
        if use_gpu:
            self.model_thzh = self.model_thzh.cuda()

    def translate(self, text: str) -> str:
        """
        Translate text from Thai to Chinese

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Thai to Chinese::

            from pythainlp.translate import ThZhTranslator

            thzh = ThZhTranslator()

            thzh.translate("ผมรักคุณ")
            # output: 我爱你

        """
        self.translated = self.model_thzh.generate(**self.tokenizer_thzh(text, return_tensors='pt', padding=True))
        return [self.tokenizer_thzh.decode(t, skip_special_tokens=True) for t in self.translated][0]