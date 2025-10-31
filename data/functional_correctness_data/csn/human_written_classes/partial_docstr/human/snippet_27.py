from sklearn.preprocessing import StandardScaler

class KerasWrap:
    """A wrapper that allows us to set parameters in the constructor and do a reset before fitting."""

    def __init__(self, model, epochs, flatten_output=False):
        self.model = model
        self.epochs = epochs
        self.flatten_output = flatten_output
        self.init_weights = None
        self.scaler = StandardScaler()

    def fit(self, X, y, verbose=0):
        if self.init_weights is None:
            self.init_weights = self.model.get_weights()
        else:
            self.model.set_weights(self.init_weights)
        self.scaler.fit(X)
        return self.model.fit(X, y, epochs=self.epochs, verbose=verbose)

    def predict(self, X):
        X = self.scaler.transform(X)
        if self.flatten_output:
            return self.model.predict(X).flatten()
        else:
            return self.model.predict(X)