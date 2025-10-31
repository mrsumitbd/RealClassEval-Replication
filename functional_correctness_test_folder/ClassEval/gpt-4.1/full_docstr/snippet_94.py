
import numpy as np


class VectorUtil:
    """
    The class provides vector operations, including calculating similarity, cosine similarities, average similarity, and IDF weights.
    """

    @staticmethod
    def similarity(vector_1, vector_2):
        """
        Compute the cosine similarity between one vector and another vector.
        """
        v1 = np.asarray(vector_1)
        v2 = np.asarray(vector_2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(v1, v2) / (norm1 * norm2))

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        """
        Compute cosine similarities between one vector and a set of other vectors.
        """
        v1 = np.asarray(vector_1)
        v1_norm = np.linalg.norm(v1)
        if v1_norm == 0:
            return np.zeros(len(vectors_all))
        sims = []
        for v2 in vectors_all:
            v2 = np.asarray(v2)
            norm2 = np.linalg.norm(v2)
            if norm2 == 0:
                sims.append(0.0)
            else:
                sims.append(np.dot(v1, v2) / (v1_norm * norm2))
        return np.array(sims)

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        """
        Compute cosine similarity between two sets of vectors.
        """
        if not vector_list_1 or not vector_list_2:
            return 0.0
        arr1 = np.array(vector_list_1)
        arr2 = np.array(vector_list_2)
        mean1 = np.mean(arr1, axis=0)
        mean2 = np.mean(arr2, axis=0)
        norm1 = np.linalg.norm(mean1)
        norm2 = np.linalg.norm(mean2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(mean1, mean2) / (norm1 * norm2))

    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
        """
        Calculate log(total_num+1/count+1) for each count in number_dict
        """
        import math
        result = {}
        for k, v in number_dict.items():
            result[k] = math.log((total_num + 1) / (v + 1))
        return result
