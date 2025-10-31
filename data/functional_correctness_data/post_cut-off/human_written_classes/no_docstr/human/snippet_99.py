import subprocess
from pathlib import Path
import os
from build_helpers import create_symlink_rel, get_base_dir, get_cmake_dir, softlink_apply_patches, copy_file

class BackendInstaller:

    @staticmethod
    def prepare(backend_name: str, backend_src_dir: str=None, is_external: bool=False):
        if not is_external:
            root_dir = os.path.join(get_base_dir(), '3rdparty', 'triton', 'third_party')
            assert backend_name in os.listdir(root_dir), f'{backend_name} is requested for install but not present in {root_dir}'
            if is_git_repo():
                try:
                    subprocess.run(['git', 'submodule', 'update', '--init', f'{backend_name}'], check=True, stdout=subprocess.DEVNULL, cwd=root_dir)
                except subprocess.CalledProcessError:
                    pass
                except FileNotFoundError:
                    pass
            backend_src_dir = os.path.join(root_dir, backend_name)
        backend_path = os.path.join(backend_src_dir, 'backend')
        assert os.path.exists(backend_path), f'{backend_path} does not exist!'
        language_dir = os.path.join(backend_src_dir, 'language')
        if not os.path.exists(language_dir):
            language_dir = None
        tools_dir = os.path.join(backend_src_dir, 'tools')
        if not os.path.exists(tools_dir):
            tools_dir = None
        for file in ['compiler.py', 'driver.py']:
            assert os.path.exists(os.path.join(backend_path, file)), f'${file} does not exist in ${backend_path}'
        install_dir = os.path.join(os.path.dirname(__file__), os.pardir, '3rdparty', 'triton', 'python', 'triton', 'backends', backend_name)
        dist_backend_path = None
        dist_language_dir = None
        return Backend(name=backend_name, src_dir=backend_src_dir, backend_dir=backend_path, language_dir=language_dir, tools_dir=tools_dir, install_dir=install_dir, is_external=is_external, dist_backend_dir=dist_backend_path, dist_language_dir=dist_language_dir)

    @staticmethod
    def copy(active):
        return [BackendInstaller.prepare(backend) for backend in active]

    @staticmethod
    def copy_externals():
        backend_dirs = os.getenv('TRITON_PLUGIN_DIRS')
        if backend_dirs is None:
            return []
        backend_dirs = backend_dirs.strip().split(';')
        backend_names = [Path(os.path.join(dir, 'backend', 'name.conf')).read_text().strip() for dir in backend_dirs]
        return [BackendInstaller.prepare(backend_name, backend_src_dir=backend_src_dir, is_external=True) for backend_name, backend_src_dir in zip(backend_names, backend_dirs)]