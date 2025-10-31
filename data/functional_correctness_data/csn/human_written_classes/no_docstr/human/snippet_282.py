from django.core.files.base import File
from django.contrib.staticfiles.utils import matches_patterns
from io import BytesIO
import gzip

class GZIPMixin:
    gzip_patterns = ('*.css', '*.js')

    def _compress(self, original_file):
        content = BytesIO()
        gzip_file = gzip.GzipFile(mode='wb', fileobj=content)
        gzip_file.write(original_file.read())
        gzip_file.close()
        content.seek(0)
        return File(content)

    def post_process(self, paths, dry_run=False, **options):
        super_class = super()
        if hasattr(super_class, 'post_process'):
            for name, hashed_name, processed in super_class.post_process(paths.copy(), dry_run, **options):
                if hashed_name != name:
                    paths[hashed_name] = (self, hashed_name)
                yield (name, hashed_name, processed)
        if dry_run:
            return
        for path in paths:
            if path:
                if not matches_patterns(path, self.gzip_patterns):
                    continue
                original_file = self.open(path)
                gzipped_path = f'{path}.gz'
                if self.exists(gzipped_path):
                    self.delete(gzipped_path)
                gzipped_file = self._compress(original_file)
                gzipped_path = self.save(gzipped_path, gzipped_file)
                yield (gzipped_path, gzipped_path, True)