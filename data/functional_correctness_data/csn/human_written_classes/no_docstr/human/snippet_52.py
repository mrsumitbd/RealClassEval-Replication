class conv_layer:

    def __init__(self, kernel_shape, num_filters):
        self.kernel_shape = kernel_shape
        self.num_filters = num_filters

    def forward_pass(self, inputs, param_vector):
        params = self.parser.get(param_vector, 'params')
        biases = self.parser.get(param_vector, 'biases')
        conv = convolve(inputs, params, axes=([2, 3], [2, 3]), dot_axes=([1], [0]), mode='valid')
        return conv + biases

    def build_weights_dict(self, input_shape):
        self.parser = WeightsParser()
        self.parser.add_weights('params', (input_shape[0], self.num_filters) + self.kernel_shape)
        self.parser.add_weights('biases', (1, self.num_filters, 1, 1))
        output_shape = (self.num_filters,) + self.conv_output_shape(input_shape[1:], self.kernel_shape)
        return (self.parser.N, output_shape)

    def conv_output_shape(self, A, B):
        return (A[0] - B[0] + 1, A[1] - B[1] + 1)