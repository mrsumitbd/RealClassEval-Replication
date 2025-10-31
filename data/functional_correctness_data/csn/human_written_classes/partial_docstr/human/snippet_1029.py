class SequenceSearchResult:
    QUERY_FROM_FIELD = 'query_from'
    QUERY_TO_FIELD = 'query_to'
    QUERY_LENGTH_FIELD = 'query_length'
    HIT_FROM_FIELD = 'hit_from'
    HIT_TO_FIELD = 'hit_to'
    ALIGNMENT_LENGTH_FIELD = 'alignment_length'
    ALIGNMENT_BIT_SCORE = 'alignment_bit_score'
    ALIGNMENT_DIRECTION = 'alignment_direction'
    HIT_ID_FIELD = 'hit_id'
    QUERY_ID_FIELD = 'query_id'
    HMM_NAME_FIELD = 'hmm_name'
    ACCESSION_ID_FIELD = 'accession_id'
    PERCENT_ID_FIELD = 'percent_id'
    MISMATCH_FIELD = 'mismatch'
    EVALUE_FIELD = 'evalue'

    def __init__(self):
        self.fields = []
        self.results = []

    def each(self, field_names):
        """Iterate over the results, yielding a list for each result, where
        each element corresponds to the field given in the field_name parameters

        Parameters
        ----------
        field_names: list of str
            The names of the fields to be returned during iteration

        Returns
        -------
        None

        Exceptions
        ----------
        raises something when a field name is not in self.fields
        """
        field_ids = []
        for f in field_names:
            field_ids.append(self.fields.index(f))
        for r in self.results:
            yield [r[i] for i in field_ids]