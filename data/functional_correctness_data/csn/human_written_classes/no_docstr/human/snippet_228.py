import os

class Editor:

    def __init__(self, editor=None, env=None, require_save=True, extension='.txt'):
        self.editor = editor
        self.env = env
        self.require_save = require_save
        self.extension = extension

    def get_editor(self):
        if self.editor is not None and self.editor.lower() != 'default':
            return self.editor
        for key in ('VISUAL', 'EDITOR'):
            rv = os.environ.get(key)
            if rv:
                return rv
        if WIN:
            return 'notepad'
        for editor in ('vim', 'nano'):
            if os.system('which %s >/dev/null 2>&1' % editor) == 0:
                return editor
        return 'vi'

    def edit_file(self, filename):
        import subprocess
        editor = self.get_editor()
        if self.env:
            environ = os.environ.copy()
            environ.update(self.env)
        else:
            environ = None
        try:
            c = subprocess.Popen('%s "%s"' % (editor, filename), env=environ, shell=True)
            exit_code = c.wait()
            if exit_code != 0:
                raise Exception('%s: Editing failed!' % editor)
        except OSError as e:
            raise Exception('%s: Editing failed: %s' % (editor, e))

    def edit(self, text):
        import tempfile
        text = text or ''
        if text and (not text.endswith('\n')):
            text += '\n'
        fd, name = tempfile.mkstemp(prefix='editor-', suffix=self.extension)
        try:
            if WIN:
                encoding = 'utf-8-sig'
                text = text.replace('\n', '\r\n')
            else:
                encoding = 'utf-8'
            text = text.encode(encoding)
            f = os.fdopen(fd, 'wb')
            f.write(text)
            f.close()
            timestamp = os.path.getmtime(name)
            self.edit_file(name)
            if self.require_save and os.path.getmtime(name) == timestamp:
                return None
            f = open(name, 'rb')
            try:
                rv = f.read()
            finally:
                f.close()
            return rv.decode('utf-8-sig').replace('\r\n', '\n')
        finally:
            os.unlink(name)