class ZhThTranslator:
    """
    Chinese-Thai Machine Translation

    from Lalita @ AI builder

    - GitHub: https://github.com/LalitaDeelert/lalita-mt-zhth
    - Facebook post https://web.facebook.com/aibuildersx/posts/166736255494822

    :param bool use_gpu : load model using GPU (Default is False)
    """

    def __init__(self, use_gpu: bool=False, pretrained: str='Lalita/marianmt-zh_cn-th') -> None:
        self.tokenizer_zhth = AutoTokenizer.from_pretrained(pretrained)
        self.model_zhth = AutoModelForSeq2SeqLM.from_pretrained(pretrained)
        if use_gpu:
            self.model_zhth.cuda()

    def translate(self, text: str) -> str:
        """
        Translate text from Chinese to Thai

        :param str text: input text in source language
        :return: translated text in target language
        :rtype: str

        :Example:

        Translate text from Chinese to Thai::

            from pythainlp.translate import ZhThTranslator

            zhth = ZhThTranslator()

            zhth.translate("我爱你")
            # output: ผมรักคุณนะ

        """
        self.translated = self.model_zhth.generate(**self.tokenizer_zhth(text, return_tensors='pt', padding=True))
        return [self.tokenizer_zhth.decode(t, skip_special_tokens=True) for t in self.translated][0]