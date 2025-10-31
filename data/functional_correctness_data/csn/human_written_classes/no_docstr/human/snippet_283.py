class PipelineMixin:
    packing = True

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return
        from pipeline.packager import Packager
        packager = Packager(storage=self)
        for package_name in packager.packages['css']:
            package = packager.package_for('css', package_name)
            output_file = package.output_filename
            if self.packing:
                packager.pack_stylesheets(package)
            paths[output_file] = (self, output_file)
            yield (output_file, output_file, True)
        for package_name in packager.packages['js']:
            package = packager.package_for('js', package_name)
            output_file = package.output_filename
            if self.packing:
                packager.pack_javascripts(package)
            paths[output_file] = (self, output_file)
            yield (output_file, output_file, True)
        super_class = super()
        if hasattr(super_class, 'post_process'):
            yield from super_class.post_process(paths.copy(), dry_run, **options)

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name