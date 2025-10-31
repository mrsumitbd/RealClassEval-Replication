import torch

class LinearRegression:

    def __init__(self):
        """
        初始化线性回归模型。
        """
        self.weight = None
        self.bias = None

    def fit(self, X, y):
        """
        使用普通最小二乘法拟合线性模型。

        参数:
        ----------
        X : array-like, shape (n_samples, n_features)
            训练数据。
        y : array-like, shape (n_samples,)
            目标值。
        """
        X = torch.as_tensor(X, dtype=torch.float64)
        y = torch.as_tensor(y, dtype=torch.float64)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        ones_column = torch.ones(X.shape[0], 1, dtype=X.dtype)
        X_b = torch.cat([X, ones_column], dim=1)
        solution = torch.linalg.lstsq(X_b, y)
        coeffs = solution.solution
        self.weight = coeffs[:-1]
        self.bias = coeffs[-1]
        return self

    def predict(self, X):
        """
        使用训练好的模型进行预测。

        参数:
        ----------
        X : array-like, shape (n_samples, n_features)
            待预测的数据。

        返回:
        -------
        y_pred : torch.Tensor, shape (n_samples,)
            预测结果。
        """
        if self.weight is None or self.bias is None:
            raise RuntimeError('模型尚未训练，请先调用 fit() 方法。')
        X = torch.as_tensor(X, dtype=torch.float64)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        return X @ self.weight + self.bias

    def serialize(self):
        """将模型参数序列化为字典。"""
        return {'weight': self.weight, 'bias': self.bias}

    @classmethod
    def deserialize(cls, data):
        """从字典加载模型参数。"""
        model = cls()
        model.weight = data['weight']
        model.bias = data['bias']
        return model

    def save_model(self, model_path):
        torch.save(self.serialize(), model_path)

    @classmethod
    def load_model(cls, model_path):
        data = torch.load(model_path)
        return cls.deserialize(data)