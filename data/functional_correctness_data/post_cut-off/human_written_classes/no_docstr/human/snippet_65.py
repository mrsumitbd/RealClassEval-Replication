import platform
from packaging.version import parse as parse_version
import subprocess
import sys

class NunchakuWheelInstaller:
    OUTPUT_NODE = True
    FUNCTION = 'run'
    CATEGORY = 'Nunchaku'
    TITLE = 'Nunchaku Installer'

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        from time import time
        return time()

    @classmethod
    def INPUT_TYPES(cls):
        return {'required': {'source': (['github', 'huggingface', 'modelscope'], {}), 'version': (OFFICIAL_VERSIONS, {}), 'dev_version_github': (DEV_CHOICES, {'default': 'None'}), 'backend': (['pip', 'uv'], {})}}
    RETURN_TYPES = ('STRING',)
    RETURN_NAMES = ('status',)

    def run(self, source: str, version: str, dev_version_github: str, backend: str):
        try:
            if is_nunchaku_installed():
                print('An existing version of Nunchaku was detected. Attempting to uninstall automatically...')
                uninstall_command = [sys.executable, '-m', 'pip', 'uninstall', 'nunchaku', '-y']
                process = subprocess.Popen(uninstall_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                output_log = []
                for line in iter(process.stdout.readline, ''):
                    print(line, end='')
                    output_log.append(line)
                process.wait()
                if process.returncode != 0:
                    full_log = ''.join(output_log)
                    raise subprocess.CalledProcessError(process.returncode, uninstall_command, output=full_log)
                status_message = '✅ An existing version of Nunchaku was detected and uninstalled.\n\n**Please restart ComfyUI completely.**\n\nThen, run this node again to install the desired version.'
                return (status_message,)
            if dev_version_github != 'None':
                final_version_tag = f'v{dev_version_github}'
                source = 'github'
            else:
                final_version_tag = 'latest' if version == 'latest' else f'v{version}'
            sys_info = get_system_info()
            if sys_info['os'] == 'unsupported':
                raise RuntimeError(f'Unsupported OS: {platform.system()}')
            source_versions = ALL_RELEASES_DATA.get(source, {})
            if final_version_tag == 'latest':
                official_tags = [v.lstrip('v') for v in source_versions.keys() if 'dev' not in v]
                if not official_tags:
                    raise RuntimeError(f"No official versions found on source '{source}'.")
                final_version_tag = f'v{sorted(official_tags, key=parse_version, reverse=True)[0]}'
            release_data = source_versions.get(final_version_tag)
            if not release_data:
                available_on = [s for s, data in ALL_RELEASES_DATA.items() if final_version_tag in data]
                msg = f"Version '{final_version_tag}' not available from '{source}'."
                if available_on:
                    msg += f' Try sources: {available_on}'
                raise RuntimeError(msg)
            assets = release_data.get('assets', [])
            if not assets:
                raise RuntimeError(f"No downloadable files found for version '{final_version_tag}'.")
            wheel_to_install = find_compatible_wheel(assets, sys_info)
            if not wheel_to_install:
                raise RuntimeError('Could not find a compatible wheel for your system.')
            log = install_wheel(wheel_to_install['url'], backend)
            status_message = f"✅ Success! Installed: {wheel_to_install['name']}\n\nRestart completely ComfyUI to apply changes.\n\n--- LOG ---\n{log}"
        except Exception as e:
            print(f'\n❌ An error occurred during installation:\n{e}')
            status_message = f'❌ ERROR:\n{str(e)}'
        return (status_message,)