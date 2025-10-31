
class patch_obj:
    """
    A simple representation of a GNU diff patch.

    The patch is stored as a list of diff hunks.  Each hunk is a dictionary
    with the following keys:

        - old_start: 1‑based index of the first line in the original file
        - old_count: number of lines in the original file that the hunk covers
        - new_start: 1‑based index of the first line in the new file
        - new_count: number of lines in the new file that the hunk covers
        - lines: a list of strings, each prefixed with one of
                 ' ', '-', or '+' to indicate context, deletion, or addition.

    Example of a hunk:

        {
            'old_start': 10,
            'old_count': 3,
            'new_start': 12,
            'new_count': 4,
            'lines': [
                ' context line 1',
                '-removed line',
                '+added line',
                ' context line 2',
            ]
        }
    """

    def __init__(self):
        """Initializes with an empty list of diffs."""
        self.diffs = []

    def __str__(self):
        """
        Emulate GNU diff's format.
        Header: @@ -382,8 +481,9 @@
        Indices are printed as 1-based, not 0-based.
        Returns:
            The GNU diff string.
        """
        if not self.diffs:
            return ""

        parts = []
        for hunk in self.diffs:
            # Header
            old_start = hunk.get("old_start", 0)
            old_count = hunk.get("old_count", 0)
            new_start = hunk.get("new_start", 0)
            new_count = hunk.get("new_count", 0)
            header = f"@@ -{old_start},{old_count} +{new_start},{new_count} @@"
            parts.append(header)

            # Lines
            for line in hunk.get("lines", []):
                # Ensure the line starts with a diff marker
                if not line or line[0] not in (" ", "+", "-"):
                    # If the line is missing a marker, treat it as context
                    parts.append(" " + line)
                else:
                    parts.append(line)

        return "\n".join(parts)
