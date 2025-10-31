from underthesea.utils import logger
from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests

class VLSPDictionary:

    def __init__(self):
        pass

    @staticmethod
    def lookups(keywords, n_workers=None):
        with Pool(n_workers) as p:
            data = p.map(VLSPDictionary.lookup, keywords)
        return data

    @staticmethod
    def lookup(keyword, cache=None):
        if cache:
            if cache.contains(keyword):
                return cache.get(keyword)
        logger.info('request ' + keyword)
        url = 'https://vlsp.hpda.vn/demo/?page=vcl'
        payload = {'word': keyword}
        r = requests.post(url, data=payload)
        soup = BeautifulSoup(r.content, 'html.parser')
        senses_data = soup.select('#vcl_content table .sense')
        if len(senses_data) == 0:
            if cache:
                cache.add(keyword, None)
            return None
        w = Word(keyword, senses=[])
        for sense_data in senses_data:
            tags = sense_data.select('.word_description li')
            syntax_tag = tags[1]
            semantic_tag = tags[2]
            syntax_tag = syntax_tag.select('font')
            tag, sub_tag = (syntax_tag[0].text, syntax_tag[1].text)
            description = ' / '.join([item.text for item in semantic_tag.select('font')])
            sense = Sense(tag, sub_tag, description)
            w.add_sense(sense)
            if cache:
                cache.add(keyword, w)
        return w