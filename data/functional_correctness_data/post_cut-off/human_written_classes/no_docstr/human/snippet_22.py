import torch

class Validator:

    def __init__(self, url, force_onnx_cpu):
        self.onnx = True if url.endswith('.onnx') else False
        torch.hub.download_url_to_file(url, 'inf.model')
        if self.onnx:
            import onnxruntime
            if force_onnx_cpu and 'CPUExecutionProvider' in onnxruntime.get_available_providers():
                self.model = onnxruntime.InferenceSession('inf.model', providers=['CPUExecutionProvider'])
            else:
                self.model = onnxruntime.InferenceSession('inf.model')
        else:
            self.model = init_jit_model(model_path='inf.model')

    def __call__(self, inputs: torch.Tensor):
        with torch.no_grad():
            if self.onnx:
                ort_inputs = {'input': inputs.cpu().numpy()}
                outs = self.model.run(None, ort_inputs)
                outs = [torch.Tensor(x) for x in outs]
            else:
                outs = self.model(inputs)
        return outs