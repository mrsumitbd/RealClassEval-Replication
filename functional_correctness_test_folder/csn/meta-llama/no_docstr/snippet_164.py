
class patch_obj:

    def __init__(self, patch_id=None, patch_name=None, patch_description=None, patch_status=None):
        self.patch_id = patch_id
        self.patch_name = patch_name
        self.patch_description = patch_description
        self.patch_status = patch_status

    def __str__(self):
        return f"Patch ID: {self.patch_id}\nPatch Name: {self.patch_name}\nPatch Description: {self.patch_description}\nPatch Status: {self.patch_status}"


# Example usage:
if __name__ == "__main__":
    patch = patch_obj(1, "Security Patch",
                      "This is a security patch.", "Applied")
    print(patch)
