import numpy as np


class VectorUtil:
    """
    The class provides vector operations, including calculating similarity, cosine similarities, average similarity, and IDF weights.
    """

    @staticmethod
    def similarity(vector_1, vector_2):
        """
        Compute the cosine similarity between one vector and another vector.
        :param vector_1: numpy.ndarray, Vector from which similarities are to be computed, expected shape (dim,).
        :param vector_2: numpy.ndarray, Vector from which similarities are to be computed, expected shape (dim,).
        :return: numpy.ndarray, Contains cosine distance between `vector_1` and `vector_2`
        >>> vector_1 = np.array([1, 1])
        >>> vector_2 = np.array([1, 0])
        >>> VectorUtil.similarity(vector_1, vector_2)
        0.7071067811865475
        """
        v1 = np.asarray(vector_1, dtype=float).ravel()
        v2 = np.asarray(vector_2, dtype=float).ravel()
        if v1.shape != v2.shape:
            raise ValueError("Vectors must have the same shape.")
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        return float(np.dot(v1, v2) / (norm1 * norm2))

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        """
        Compute cosine similarities between one vector and a set of other vectors.
        :param vector_1: numpy.ndarray, Vector from which similarities are to be computed, expected shape (dim,).
        :param vectors_all: list of numpy.ndarray, For each row in vectors_all, distance from vector_1 is computed, expected shape (num_vectors, dim).
        :return: numpy.ndarray, Contains cosine distance between `vector_1` and each row in `vectors_all`, shape (num_vectors,).
        >>> vector1 = np.array([1, 2, 3])
        >>> vectors_all = [np.array([4, 5, 6]), np.array([7, 8, 9])]
        >>> VectorUtil.cosine_similarities(vector1, vectors_all)
        [0.97463185 0.94491118]
        """
        v1 = np.asarray(vector_1, dtype=float).ravel()
        if len(vectors_all) == 0:
            return np.array([], dtype=float)
        mat = np.vstack([np.asarray(v, dtype=float).ravel()
                        for v in vectors_all])
        if mat.shape[1] != v1.shape[0]:
            raise ValueError("All vectors must have the same dimensionality.")
        v1_norm = np.linalg.norm(v1)
        mat_norms = np.linalg.norm(mat, axis=1)
        denom = v1_norm * mat_norms
        # Avoid division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            sims = np.dot(mat, v1) / denom
            sims = np.where((denom == 0) | (v1_norm == 0), 0.0, sims)
        return sims

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        """
        Compute cosine similarity between two sets of vectors.
        :param vector_list_1: list of numpy vector
        :param vector_list_2: list of numpy vector
        :return: numpy.ndarray, Similarities between vector_list_1 and vector_list_2.
        >>> vector_list1 = [np.array([1, 2, 3]), np.array([4, 5, 6])]
        >>> vector_list2 = [np.array([7, 8, 9]), np.array([10, 11, 12])]
        >>> VectorUtil.n_similarity(vector_list1, vector_list2)
        0.9897287473881233
        """
        if len(vector_list_1) == 0 or len(vector_list_2) == 0:
            return 0.0
        mat1 = np.vstack([np.asarray(v, dtype=float).ravel()
                         for v in vector_list_1])
        mat2 = np.vstack([np.asarray(v, dtype=float).ravel()
                         for v in vector_list_2])
        if mat1.shape[1] != mat2.shape[1]:
            raise ValueError(
                "Vectors in both lists must have the same dimensionality.")
        mean1 = mat1.mean(axis=0)
        mean2 = mat2.mean(axis=0)
        return VectorUtil.similarity(mean1, mean2)

    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
        """
        Calculate log(total_num+1/count+1) for each count in number_dict
        :param total_num: int
        :param number_dict: dict
        :return: dict
        >>> num_dict = {'key1':0.1, 'key2':0.5}
        >>> VectorUtil.compute_idf_weight_dict(2, num_dict)
        {'key1': 1.0033021088637848, 'key2': 0.6931471805599453}
        """
        if total_num < 0:
            raise ValueError("total_num must be non-negative.")
        result = {}
        for k, v in number_dict.items():
            count = float(v)
            result[k] = float(np.log((total_num + 1.0) / (count + 1.0)))
        return result
