class LabelEncoder:

    def __init__(self):
        self.index2label = {}
        self.label2index = {}
        self.vocab_size = 0

    def encode(self, labels):
        if type(labels) is list:
            return [self.encode(label) for label in labels]
        label = labels
        if label not in self.label2index:
            index = self.vocab_size
            self.label2index[label] = index
            self.index2label[index] = label
            self.vocab_size += 1
            return index
        else:
            return self.label2index[label]