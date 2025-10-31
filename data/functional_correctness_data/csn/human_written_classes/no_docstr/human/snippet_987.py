from pathlib import Path

class MusicLibrary:

    def __init__(self, name, paths=None, excludes=None, sync=True):
        self.name = name
        self.paths = paths or []
        self.sync = sync
        self.excludes = excludes

    @staticmethod
    def fromConfig(config):
        all_paths = []
        paths = config.get('paths')
        if paths:
            paths = paths.split('\n')
            for p in [Path(p).expanduser() for p in paths]:
                glob_paths = [str(p) for p in Path('/').glob(str(p.relative_to('/')))]
                all_paths += glob_paths if glob_paths else [str(p)]
        excludes = [str(Path(p).expanduser()) for p in config.getlist('excludes', fallback=[])]
        return MusicLibrary(config.name.split(':', 1)[1], paths=all_paths, excludes=excludes, sync=config.getboolean('sync', True))