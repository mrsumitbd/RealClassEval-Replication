import re

class Capitalizer:
    KEYWORD_RE = '(?:"\\w+)|(?:\\\'\\w+)|\\w+'

    def __init__(self, cmd, completer):
        self.cmd = cmd
        self.last_changed = None
        self.completer = completer

    def apply_capitalization(self, buffer):
        if not self.cmd.should_autocapitalize():
            return
        current_line = buffer.document.text
        if current_line.startswith('\\'):
            return
        cursor_position = buffer.document.cursor_position
        if self.last_changed and self.is_prefix(current_line[:cursor_position].lower(), self.last_changed.lower()):
            diff = len(self.last_changed) - len(current_line)
            current_line = self.last_changed + current_line[diff:]
        new_line = re.sub(self.KEYWORD_RE, self.keyword_replacer, current_line[:cursor_position])
        if new_line != buffer.document.text:
            buffer.delete_before_cursor(cursor_position)
            buffer.delete(len(new_line) - cursor_position)
            buffer.insert_text(new_line, overwrite=False, move_cursor=True, fire_event=False)
            self.last_changed = current_line[:cursor_position]

    def keyword_replacer(self, match):
        if match.group(0).lower() in self.completer.keywords:
            return match.group(0).upper()
        else:
            return match.group(0)

    def is_prefix(self, string, prefix):
        return string.startswith(prefix) and string != prefix