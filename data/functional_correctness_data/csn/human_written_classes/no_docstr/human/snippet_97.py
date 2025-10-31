import dynet as dy

class LSTMLM:

    def __init__(self, model, vocab_size, start):
        self.start = start
        self.embeddings = model.add_lookup_parameters((vocab_size, FLAGS_word_dim))
        self.rnn = dy.VanillaLSTMBuilder(FLAGS_layers, FLAGS_word_dim, FLAGS_hidden_dim, model)
        self.h2l = model.add_parameters((vocab_size, FLAGS_hidden_dim))
        self.lb = model.add_parameters(vocab_size)

    def sent_lm_loss(self, sent):
        rnn_cur = self.rnn.initial_state()
        losses = []
        prev_word = self.start
        for word in sent:
            x_t = self.embeddings[prev_word]
            rnn_cur = rnn_cur.add_input(x_t)
            logits = dy.affine_transform([self.lb, self.h2l, rnn_cur.output()])
            losses.append(dy.pickneglogsoftmax(logits, word))
            prev_word = word
        return dy.esum(losses)

    def minibatch_lm_loss(self, sents):
        sent_losses = [self.sent_lm_loss(sent) for sent in sents]
        minibatch_loss = dy.esum(sent_losses)
        total_words = sum((len(sent) for sent in sents))
        return (minibatch_loss, total_words)