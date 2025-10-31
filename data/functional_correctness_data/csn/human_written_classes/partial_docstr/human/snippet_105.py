from s_tui.sources.hook_script import ScriptHook
import os

class ScriptHookLoader:
    """
    Loads shell scripts from a directory into ScriptHooks for a given Source
    """

    def __init__(self, dir_path):
        self.scripts_dir_path = os.path.join(dir_path, 'hooks.d')

    def load_script(self, source_name, timeoutMilliseconds=0):
        """
        Return ScriptHook for source_name Source and with a ready timeout
        of timeoutMilliseconds
        """
        script_path = os.path.join(self.scripts_dir_path, self._source_to_script_name(source_name))
        if os.path.isfile(script_path):
            return ScriptHook(script_path, timeoutMilliseconds)
        return None

    def _source_to_script_name(self, source_name):
        return source_name.lower() + '.sh'