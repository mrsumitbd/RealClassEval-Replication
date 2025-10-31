import distutils.core
import os.path
import setuptools.command.build_ext
import distutils.cmd

class MyBuildExtCommand(setuptools.command.build_ext.build_ext):
    """Compile Kappa agent in addition of standard build"""

    def append_a_binary(self, bin_dir, name):
        file_in_src = os.path.realpath(os.path.join('bin', name))
        if os.path.isfile(file_in_src):
            distutils.file_util.copy_file(file_in_src, os.path.join(bin_dir, name))
            self.my_outputs.append(os.path.join(bin_dir, name))

    def run(self):
        self.my_outputs = []
        self.run_command('build_agents')
        bin_dir = os.path.join(self.build_lib, 'kappy/bin')
        distutils.dir_util.mkpath(bin_dir)
        self.append_a_binary(bin_dir, 'KaSimAgent')
        self.append_a_binary(bin_dir, 'KappaSwitchman')
        self.append_a_binary(bin_dir, 'KaSaAgent')
        self.append_a_binary(bin_dir, 'KaMoHa')
        setuptools.command.build_ext.build_ext.run(self)

    def get_outputs(self):
        outputs = setuptools.command.build_ext.build_ext.get_outputs(self)
        outputs.extend(self.my_outputs)
        return outputs