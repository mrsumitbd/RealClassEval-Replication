class CONLLReader:

    @staticmethod
    def load(file):
        sentences = open(file).read().split('\n\n')
        sentences = [s.strip() for s in sentences if len(s) > 10]
        return sentences

    @staticmethod
    def save(sentences, file):
        n = len(sentences)
        content = '\n\n'.join(sentences) + '\n'
        print(f'Save {n} sentences in {file}')
        with open(file, 'w') as f:
            f.write(content)