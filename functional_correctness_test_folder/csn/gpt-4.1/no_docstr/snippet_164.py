
class patch_obj:

    def __init__(self):
        self.patches = []

    def add_patch(self, patch):
        self.patches.append(patch)

    def __str__(self):
        return f"patch_obj({self.patches})"
