import os
from setuptools import find_packages, monkey, setup, Extension
from distutils import log as logger
from setuptools.command.build_ext import build_ext as build_ext_orig
import subprocess

class build_ext(build_ext_orig):

    def run(self):
        monkey.patch_all()
        cmake_build_dir = None
        for ext in self.extensions:
            if isinstance(ext, UAMQPExtension):
                self.build_cmake(ext)
                cmake_build_dir = self.cmake_build_dir
            else:
                ext.library_dirs += [cmake_build_dir, cmake_build_dir + '/deps/azure-c-shared-utility/', cmake_build_dir + '/Debug/', cmake_build_dir + '/Release/', cmake_build_dir + '/deps/azure-c-shared-utility/Debug/', cmake_build_dir + '/deps/azure-c-shared-utility/Release/']
        build_ext_orig.run(self)

    def build_cmake(self, ext):
        cwd = os.getcwd()
        self.cmake_build_dir = self.build_temp + '/cmake'
        create_folder_no_exception(self.cmake_build_dir)
        extdir = self.get_ext_fullpath(ext.name)
        create_folder_no_exception(extdir)
        logger.info('will build uamqp in %s', self.cmake_build_dir)
        os.chdir(cwd + '/' + self.cmake_build_dir)
        generator_flags = get_generator_flags()
        logger.info('Building with generator flags: {}'.format(generator_flags))
        build_env = get_build_env()
        configure_command = ['cmake', cwd + '/src/vendor/azure-uamqp-c/', generator_flags, '-Duse_openssl:bool={}'.format('ON' if use_openssl else 'OFF'), '-Duse_default_uuid:bool=ON ', '-Duse_builtin_httpapi:bool=ON ', '-Dskip_samples:bool=ON', '-DCMAKE_POSITION_INDEPENDENT_CODE=TRUE', '-DCMAKE_BUILD_TYPE=Release']
        joined_cmd = ' '.join(configure_command)
        logger.info('calling %s', joined_cmd)
        subprocess.check_call(joined_cmd, shell=True, universal_newlines=True, env=build_env)
        compile_command = ['cmake', '--build', '.', '--config', 'Release']
        joined_cmd = ' '.join(compile_command)
        logger.info('calling %s', joined_cmd)
        subprocess.check_call(joined_cmd, shell=True, universal_newlines=True, env=build_env)
        os.chdir(cwd)
        if USE_CYTHON:
            create_cython_file()