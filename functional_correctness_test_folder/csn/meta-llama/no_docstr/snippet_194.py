
class EXTRACT_KEY_FROM_KEY_Mechanism:

    def __init__(self, extractParams):
        """
        Initialize the EXTRACT_KEY_FROM_KEY_Mechanism class.

        Args:
            extractParams (dict): A dictionary containing the extraction parameters.
        """
        if not isinstance(extractParams, dict):
            raise TypeError("extractParams must be a dictionary")

        required_keys = ['source_key', 'target_key']
        if not all(key in extractParams for key in required_keys):
            raise ValueError(
                "extractParams must contain 'source_key' and 'target_key'")

        self.extractParams = extractParams

    def to_native(self):
        """
        Convert the extraction parameters to a native Python dictionary.

        Returns:
            dict: A dictionary containing the extraction parameters.
        """
        native_dict = {
            'source_key': self.extractParams['source_key'],
            'target_key': self.extractParams['target_key']
        }
        return native_dict
