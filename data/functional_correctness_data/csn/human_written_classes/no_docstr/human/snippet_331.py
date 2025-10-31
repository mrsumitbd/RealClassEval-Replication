import numpy as np

class Seq2Seq_ONNX:

    def __init__(self, encoder, decoder, target_start_token, target_end_token, max_length, target_vocab_size):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.pad_idx = 0
        self.target_start_token = target_start_token
        self.target_end_token = target_end_token
        self.max_length = max_length
        self.target_vocab_size = target_vocab_size

    def create_mask(self, source_seq):
        mask = source_seq != self.pad_idx
        return mask

    def run(self, source_seq, source_seq_len):
        batch_size = source_seq.shape[0]
        start_token = self.target_start_token
        end_token = self.target_end_token
        max_len = self.max_length
        outputs = np.zeros((max_len, batch_size, self.target_vocab_size))
        expected_encoder_outputs = list(map(lambda output: output.name, self.encoder.get_outputs()))
        encoder_outputs, encoder_hidden, _ = self.encoder.run(input_feed={'input_tensor': source_seq, 'input_lengths': source_seq_len}, output_names=expected_encoder_outputs)
        decoder_input = np.array([[start_token] * batch_size]).reshape(batch_size, 1)
        encoder_hidden_h_t = np.expand_dims(np.concatenate((encoder_hidden[0], encoder_hidden[1]), axis=1), axis=0)
        decoder_hidden = encoder_hidden_h_t
        max_source_len = encoder_outputs.shape[1]
        mask = self.create_mask(source_seq[:, 0:max_source_len])
        for di in range(max_len):
            decoder_output, decoder_hidden = self.decoder.run(input_feed={'decoder_input': decoder_input.astype('int32'), 'decoder_hidden_1': decoder_hidden, 'encoder_outputs': encoder_outputs, 'mask': mask.tolist()}, output_names=[self.decoder.get_outputs()[0].name, self.decoder.get_outputs()[1].name])
            topi = np.argmax(decoder_output, axis=1)
            outputs[di] = decoder_output
            decoder_input = np.array([topi])
            if decoder_input == end_token:
                return outputs[:di]
        return outputs