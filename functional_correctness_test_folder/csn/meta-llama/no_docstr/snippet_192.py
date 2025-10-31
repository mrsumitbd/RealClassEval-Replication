
class CONCATENATE_BASE_AND_KEY_Mechanism:

    def __init__(self, encKey):
        """
        Initialize the CONCATENATE_BASE_AND_KEY_Mechanism class.

        Args:
            encKey (str): The encryption key.
        """
        self.encKey = encKey

    def to_native(self):
        """
        Concatenates the base ('CONCATENATE_BASE_AND_KEY') and the encryption key.

        Returns:
            str: The concatenated string.
        """
        base_string = 'CONCATENATE_BASE_AND_KEY'
        return base_string + self.encKey


# Example usage:
if __name__ == "__main__":
    mechanism = CONCATENATE_BASE_AND_KEY_Mechanism('my_enc_key')
    print(mechanism.to_native())  # Outputs: CONCATENATE_BASE_AND_KEYmy_enc_key
