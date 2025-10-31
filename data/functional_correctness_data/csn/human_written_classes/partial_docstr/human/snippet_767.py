class HdrIterationValue:
    """Class of the values returned by each iterator
    """

    def __init__(self, hdr_iterator):
        self.hdr_iterator = hdr_iterator
        self.value_iterated_to = 0
        self.value_iterated_from = 0
        self.count_at_value_iterated_to = 0
        self.count_added_in_this_iter_step = 0
        self.total_count_to_this_value = 0
        self.total_value_to_this_value = 0
        self.percentile = 0.0
        self.percentile_level_iterated_to = 0.0
        self.int_to_double_conversion_ratio = 0.0

    def set(self, value_iterated_to):
        hdr_it = self.hdr_iterator
        self.value_iterated_to = value_iterated_to
        self.value_iterated_from = hdr_it.prev_value_iterated_to
        self.count_at_value_iterated_to = hdr_it.count_at_this_value
        self.count_added_in_this_iter_step = hdr_it.total_count_to_current_index - hdr_it.total_count_to_prev_index
        self.total_count_to_this_value = hdr_it.total_count_to_current_index
        self.total_value_to_this_value = hdr_it.value_to_index
        self.percentile = 100.0 * hdr_it.total_count_to_current_index / hdr_it.total_count
        self.percentile_level_iterated_to = hdr_it.get_percentile_iterated_to()
        self.int_to_double_conversion_ratio = hdr_it.int_to_double_conversion_ratio