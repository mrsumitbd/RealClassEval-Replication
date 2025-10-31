import threading

class ConversionResult:

    def __init__(self):
        self.lock = threading.Lock()
        self.weight_map = {}
        self.param_count = 0
        self.modules_to_not_convert = []

    def add_result(self, filename, q_weights, module_names):
        with self.lock:
            for k, v in q_weights.items():
                self.weight_map[k] = filename
                self.param_count += len(v)
            self.modules_to_not_convert.extend(module_names)