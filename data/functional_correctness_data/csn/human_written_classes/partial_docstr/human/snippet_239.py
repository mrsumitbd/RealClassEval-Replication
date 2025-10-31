from os.path import dirname, join

class KLDivergence:

    def __init__(self, word_counter, doc_word_counters):
        """
        F: Term (word) frequency
        L_x: Frequency sum of all docs containing word
        P_c: Distribution of word in the collection
        P_x: Distribution of word in sampled docs
        """
        self.words = word_counter.keys()
        self.F = [word_counter.get(word) for word in self.words]
        self.index = invert_index(doc_word_counters)
        self.L_x = [sum(doc_word_counters[doc].values()) for word in self.words for doc in self.index[word]]
        self.P_c = [float(F) / sum(word_counter.values()) for F in self.F]
        self.P_x = [float(self.F[i]) / self.L_x[i] for i in range(len(self.F))]
        self.values = [kl_div(self.P_x[i], self.P_c[i]) for i in range(len(self.P_x))]

    def write(self):
        words = [x for _, x in sorted(zip(self.values, self.words), reverse=True)][:70]
        content = '\n'.join([s for s in words])
        target_file = join(STOPWORDS_FOLDER, 'stopwords_dev.txt')
        with open(target_file, 'w') as f:
            f.write(content)