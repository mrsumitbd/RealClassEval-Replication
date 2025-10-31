import logging
import time
from nltk.corpus import wordnet
import json
from api.utils.file_utils import get_project_base_directory
import re
import os

class Dealer:

    def __init__(self, redis=None):
        self.lookup_num = 100000000
        self.load_tm = time.time() - 1000000
        self.dictionary = None
        path = os.path.join(get_project_base_directory(), 'rag/res', 'synonym.json')
        try:
            self.dictionary = json.load(open(path, 'r', encoding='utf-8'))
        except Exception:
            logging.warning('Missing synonym.json')
            self.dictionary = {}
        if not redis:
            logging.warning('Realtime synonym is disabled, since no redis connection.')
        if not len(self.dictionary.keys()):
            logging.warning('Fail to load synonym')
        self.redis = redis
        self.load()

    def load(self):
        if not self.redis:
            return
        if self.lookup_num < 100:
            return
        tm = time.time()
        if tm - self.load_tm < 3600:
            return
        self.load_tm = time.time()
        self.lookup_num = 0
        d = self.redis.get('kevin_synonyms')
        if not d:
            return
        try:
            d = json.loads(d)
            self.dictionary = d
        except Exception as e:
            logging.error('Fail to load synonym!' + str(e))

    def lookup(self, tk, topn=8):
        """
        查找输入词条(tk)的同义词，支持英文和中文混合处理

        参数:
            tk (str): 待查询的词条（如"happy"或"苹果"）
            topn (int): 最多返回的同义词数量，默认为8

        返回:
            list: 同义词列表，可能为空（无同义词时）

        处理逻辑:
            1. 英文单词：使用WordNet语义网络查询
            2. 中文/其他：从预加载的自定义词典查询
        """
        if re.match('[a-z]+$', tk):
            res = list(set([re.sub('_', ' ', syn.name().split('.')[0]) for syn in wordnet.synsets(tk)]) - set([tk]))
            return [t for t in res if t]
        self.lookup_num += 1
        self.load()
        res = self.dictionary.get(re.sub('[ \\t]+', ' ', tk.lower()), [])
        if isinstance(res, str):
            res = [res]
        return res[:topn]