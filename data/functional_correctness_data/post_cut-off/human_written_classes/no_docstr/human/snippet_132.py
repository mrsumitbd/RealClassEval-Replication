class ConditionalWeightsManager:

    def __init__(self, weights_manager, condition):
        self.weights_manager = weights_manager
        self.condition = condition

    def update_condition(self, condition):
        self.condition = condition

    def __enter__(self):
        if self.condition:
            self.weights_manager.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.condition:
            return self.weights_manager.__exit__(exc_type, exc_val, exc_tb)
        return False