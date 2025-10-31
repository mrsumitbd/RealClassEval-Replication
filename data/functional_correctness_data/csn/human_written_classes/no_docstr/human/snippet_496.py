class PlainCodec:

    def marshal(self, value, **kwargs):
        return value

    def unmarshal(self, data, **kwargs):
        return data