import numpy as np

class Node:
    """Represents a framework-agnostic neural network layer in a directed graph."""

    def __init__(self, uid, name, op, output_shape=None, params=None):
        """
        uid: unique ID for the layer that doesn't repeat in the computation graph.
        name: Name to display
        op: Framework-agnostic operation name.
        """
        self.id = uid
        self.name = name
        self.op = op
        self.repeat = 1
        if output_shape:
            assert isinstance(output_shape, (tuple, list)), 'output_shape must be a tuple or list but received {}'.format(type(output_shape))
        self.output_shape = output_shape
        self.params = params if params else {}
        self._caption = ''

    @property
    def title(self):
        title = self.name or self.op
        if 'kernel_shape' in self.params:
            kernel = self.params['kernel_shape']
            title += 'x'.join(map(str, kernel))
        if 'stride' in self.params:
            stride = self.params['stride']
            if np.unique(stride).size == 1:
                stride = stride[0]
            if stride != 1:
                title += '/s{}'.format(str(stride))
        return title

    @property
    def caption(self):
        if self._caption:
            return self._caption
        caption = ''
        return caption

    def __repr__(self):
        args = (self.op, self.name, self.id, self.title, self.repeat)
        f = '<Node: op: {}, name: {}, id: {}, title: {}, repeat: {}'
        if self.output_shape:
            args += (str(self.output_shape),)
            f += ', shape: {:}'
        if self.params:
            args += (str(self.params),)
            f += ', params: {:}'
        f += '>'
        return f.format(*args)