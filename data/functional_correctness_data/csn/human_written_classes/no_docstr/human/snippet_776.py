from sklearn.preprocessing import LabelEncoder

class ClassDecoder:

    def __init__(self):
        self._label_encoder = LabelEncoder()

    def fit(self, classes):
        self._label_encoder.classes_ = classes

    def decode(self, y):
        return self._label_encoder.inverse_transform(y)