from nearpy.hashes.permutation.permutedIndex import PermutedIndex

class Permutation:
    """
    This class 1) stores all the permutedIndex in a dict self.permutedIndexs ({hash_name,permutedIndex}) 
    and 2) provide a method to get the neighbour bucket keys given hash_name and query bucket key.
    """

    def __init__(self):
        self.permutedIndexs = {}

    def build_permuted_index(self, lshash, buckets, num_permutation, beam_size, num_neighbour):
        """
        Build a permutedIndex and store it into the dict self.permutedIndexs.
        lshash: the binary lshash object (nearpy.hashes.lshash).
        buckets: the buckets object corresponding to lshash. It's a dict object 
                 which can get from nearpy.storage.buckets[lshash.hash_name]
        num_permutation: the number of sorted randomly-permuted bucket key lists (SRPBKL).
        beam_size: beam size, details please refer to __init__() in nearpy.hashes.permutation.PermutedIndex 
        num_neighbour: the number of neighbour bucket keys needed to return in self.get_neighbour_keys().
        """
        pi = PermutedIndex(lshash, buckets, num_permutation, beam_size, num_neighbour)
        hash_name = lshash.hash_name
        self.permutedIndexs[hash_name] = pi

    def get_neighbour_keys(self, hash_name, bucket_key):
        """
        Return the neighbour buckets given hash_name and query bucket key.
        """
        permutedIndex = self.permutedIndexs[hash_name]
        return permutedIndex.get_neighbour_keys(bucket_key, permutedIndex.num_neighbour)