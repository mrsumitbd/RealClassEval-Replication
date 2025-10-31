from typing import Optional
import json
from libs.utils.utils import CustomEncoder

class DataClassificationResult:
    """
    A class representing the result of data classification.

    Attributes:
        classification: The classification of the data.
        accuracy: The accuracy of the classification.
        execution_time: The execution time of the data classification.
    """

    def __init__(self, classification: Optional[dict], accuracy: Optional[float], execution_time: Optional[float]):
        """
        Initializes a new instance of the DataClassificationResult class.

        Args:
            classification: The classification of the data.
            accuracy: The accuracy of the classification.
            execution_time: The execution time of the data classification.
        """
        self.classification = classification
        self.accuracy = accuracy
        self.execution_time = execution_time

    def to_json(self, indent: Optional[int]=4) -> str:
        """
        Converts the DataClassificationResult object to a JSON string using a CustomEncoder for serializing objects with 'to_dict' and 'as_dict' methods.

        Args:
            indent: The number of spaces to indent the JSON string.

        Returns:
            str: The DataClassificationResult object as a JSON string.
        """
        return json.dumps(self.to_dict(), indent=indent, cls=CustomEncoder)

    def to_dict(self) -> dict:
        """
        Converts the DataClassificationResult object to a dictionary.

        Returns:
            dict: The DataClassificationResult object as a dictionary.
        """
        return {'classification': self.classification, 'accuracy': self.accuracy, 'execution_time': self.execution_time}