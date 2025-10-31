class NunchakuIPAdapterLoader:
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "load"
    CATEGORY = "Nunchaku/IP-Adapter"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}}

    def load(self, model):
        return (model,)
