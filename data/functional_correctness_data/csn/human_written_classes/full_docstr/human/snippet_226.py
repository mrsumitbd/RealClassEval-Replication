import re

class AnnotationLines:
    """
    AnnotationLines provides utility methods to work with a string in terms of
    lines.  As an example, it can convert a Call node into a list of its contents
    separated by line breaks.
    """
    _ANNOTATION_REGEX = re.compile('[\\s]*#[\\s]*\\.\\.[\\s]*(toggle)')

    def __init__(self, module_node):
        """
        Arguments:
            module_node: The visited module node.
        """
        module_as_binary = module_node.stream().read()
        file_encoding = module_node.file_encoding
        if file_encoding is None:
            file_encoding = 'UTF-8'
        module_as_string = module_as_binary.decode(file_encoding)
        self._list_of_string_lines = module_as_string.split('\n')

    def is_line_annotated(self, line_number):
        """
        Checks if the provided line number is annotated.
        """
        if line_number < 1 or self._line_count() < line_number:
            return False
        return bool(self._ANNOTATION_REGEX.match(self._get_line_contents(line_number)))

    def _line_count(self):
        """
        Gets the number of lines in the string.
        """
        return len(self._list_of_string_lines)

    def _get_line_contents(self, line_number):
        """
        Gets the line of text designated by the provided line number.
        """
        return self._list_of_string_lines[line_number - 1]