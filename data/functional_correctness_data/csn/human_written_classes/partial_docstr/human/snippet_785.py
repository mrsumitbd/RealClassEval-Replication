class ValidationResult:
    """
    Representation of the result of a validation.
    The basic result just indicates a pass or fail.
    Depending on the validator it can be extended to hold more information
    (e.g. utterance-ids which triggered the task to fail).

    Args:
        passed (bool): A boolean indicating, if the validation has passed
                       (``True``) or failed (``False``).
        name (str): The name of the validator, that produced the result.
        info (dict): Dictionary containing key/value string-pairs with detailed
                     information of the validation. For example id of the
                     label-list that was validated.
    """

    def __init__(self, passed, name='Validation', info=None):
        self.passed = passed
        self.name = name
        self.info = info

    def get_report(self):
        """
        Return a string containing a report of the result.
        This can used to print or save to a text file.

        Returns:
            str: String containing infos about the result
        """
        lines = [self.name, '=' * len(self.name)]
        if self.info is not None:
            lines.append('')
            sorted_info = sorted(self.info.items(), key=lambda x: x[0])
            lines.extend(['--> {}: {}'.format(k, v) for k, v in sorted_info])
        lines.append('')
        lines.append('Result: {}'.format('Passed' if self.passed else 'Failed'))
        return '\n'.join(lines)