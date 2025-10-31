class sequence_unique:
    """
    Object to store the sequence information like: **counts**, **sequence**, **id**
    """

    def __init__(self, idx, seq):
        self.idx = idx
        self.seq = seq
        self.group = {}
        self.quality = ''
        self.total = 0

    def add_exp(self, gr, exp):
        """Function to add the counts for each sample

        :param gr: name of the sample
        :param exp: counts of sample **gr**

        :returns: dict with key,values equally to name,counts.
        """
        self.group[gr] = exp
        self.total = sum(self.group.values())