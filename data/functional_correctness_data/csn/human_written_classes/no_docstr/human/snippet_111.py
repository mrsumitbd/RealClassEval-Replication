import setuptools.command.build_ext as _build_ext
import subprocess
import os
import shutil

class build_ext(_build_ext.build_ext):

    def run(self):
        if not os.path.exists(libweld):
            subprocess.call('cargo build --release', shell=True)
        if not is_develop_command:
            self.move_file(libweld, 'weld')

    def move_file(self, filename, directory):
        source = filename
        dir, name = os.path.split(source)
        destination = os.path.join(self.build_lib + '/' + directory + '/', name)
        print('Copying {} to {}'.format(source, destination))
        shutil.copy(source, destination)