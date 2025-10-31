class patch_obj:
    def __init__(self):
        # Initialize an empty dictionary to hold patch data
        self._patches = {}

    def __str__(self):
        # Return a readable string representation of the patch object
        return f"patch_obj(patches={self._patches})"
