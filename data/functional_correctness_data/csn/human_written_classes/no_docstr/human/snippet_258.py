import re
from os.path import join
from underthesea.file_utils import DATASETS_FOLDER
from underthesea.data_fetcher import DataFetcher

class UITABSAHotel:
    NAME = 'UIT_ABSA_HOTEL'
    VERSION = '1.0'

    def __init__(self, training='aspect'):
        DataFetcher.download_data(UITABSAHotel.NAME, None)
        train_file = join(DATASETS_FOLDER, UITABSAHotel.NAME, 'Train_Hotel.txt')
        dev_file = join(DATASETS_FOLDER, UITABSAHotel.NAME, 'Dev_Hotel.txt')
        test_file = join(DATASETS_FOLDER, UITABSAHotel.NAME, 'Test_Hotel.txt')
        print('Currently training: %s (aspect or polarity)' % training)
        self.training = training
        self.label_encoder = LabelEncoder()
        self.train = self._extract_sentences(train_file)
        self.dev = self._extract_sentences(dev_file)
        self.test = self._extract_sentences(test_file)
        self.num_labels = self.label_encoder.vocab_size

    def _join_labels(self, label):
        return '#'.join(label)

    def _extract_sentence(self, sentence):
        sentence_id, text, labels = sentence.split('\n')
        labels = re.findall('\\{(?P<aspect>.*?), (?P<polarity>.*?)\\}', labels)
        aspect_labels = [label[0] for label in labels]
        polarity_labels = [label[1] for label in labels]
        if self.training == 'aspect':
            label_ids = self.label_encoder.encode(aspect_labels)
        else:
            label_ids = self.label_encoder.encode(polarity_labels)
        return {'sentence_id': sentence_id, 'text': text, 'labels': labels, 'aspect_labels': aspect_labels, 'polarity_labels': polarity_labels, 'label_ids': label_ids}

    def _extract_sentences(self, file):
        with open(file, encoding='utf-8') as f:
            content = f.read()
            sentences = content.split('\n\n')
            sentences = [self._extract_sentence(s) for s in sentences]
        return sentences