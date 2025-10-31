from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime
import os
import shutil


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    def __init__(self):
        '''初始化快捷键命令'''
        self.marker_start = '# >>> shortcuts managed block >>>'
        self.marker_end = '# <<< shortcuts managed block <<<'
        self.base_dir = Path.home() / '.config' / 'shortcuts'
        self.user_sh_file = self.base_dir / 'shortcuts.sh'
        self.user_fish_file = self.base_dir / 'shortcuts.fish'
        self.result: Dict[str, Any] = {
            'ok': False,
            'shell': None,
            'rc_file': None,
            'created_files': [],
            'modified_files': [],
            'backups': [],
            'message': '',
            'user_shortcuts_file': None,
        }

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        try:
            shell_name = self._detect_shell(shell)
            if not shell_name:
                self.result['message'] = '无法自动检测 shell，请通过参数显式指定：bash/zsh/fish'
                self._print_result(self.result)
                return 1

            self.result['shell'] = shell_name
            self.base_dir.mkdir(parents=True, exist_ok=True)

            if shell_name in ('bash', 'zsh'):
                rc_file = self._rc_file_for(shell_name)
                self.result['rc_file'] = str(rc_file)
                # 1) 确保用户快捷键文件存在
                if not self.user_sh_file.exists():
                    default_sh = (
                        '# ~/.config/shortcuts/shortcuts.sh\n'
                        '# 在此添加你的 alias 或函数（bash/zsh）\n'
                        "# 示例：alias gs='git status'\n"
                        '# 示例：ll() { ls -alF "$@"; }\n'
                    )
                    self.user_sh_file.write_text(default_sh, encoding='utf-8')
                    self.result['created_files'].append(str(self.user_sh_file))

                # 2) 在 rc 文件中注入 managed block
                rc_file.parent.mkdir(parents=True, exist_ok=True)
                if not rc_file.exists():
                    rc_file.touch()
                    self.result['created_files'].append(str(rc_file))

                block = (
                    f'{self.marker_start}\n'
                    'if [ -f "$HOME/.config/shortcuts/shortcuts.sh" ]; then\n'
                    '  . "$HOME/.config/shortcuts/shortcuts.sh"\n'
                    'fi\n'
                    f'{self.marker_end}\n'
                )
                modified, backup = self._ensure_block(rc_file, block)
                if modified:
                    self.result['modified_files'].append(str(rc_file))
                if backup:
                    self.result['backups'].append(str(backup))

                self.result['user_shortcuts_file'] = str(self.user_sh_file)
                self.result['ok'] = True
                self.result['message'] = '已安装 shortcuts 载入块至 rc 文件'

            elif shell_name == 'fish':
                # fish: 使用 conf.d 自动加载的机制
                fish_conf_d = Path.home() / '.config' / 'fish' / 'conf.d'
                fish_conf_d.mkdir(parents=True, exist_ok=True)
                loader = fish_conf_d / 'shortcuts.fish'

                # 用户可编辑文件
                if not self.user_fish_file.exists():
                    default_fish = (
                        '# ~/.config/shortcuts/shortcuts.fish\n'
                        '# 在此添加你的 fish alias 或函数\n'
                        "# fish 示例：alias gs 'git status'\n"
                        "# fish 示例：function ll; ls -alF $argv; end\n"
                    )
                    self.user_fish_file.write_text(
                        default_fish, encoding='utf-8')
                    self.result['created_files'].append(
                        str(self.user_fish_file))

                loader_content = (
                    f'# {self.marker_start}\n'
                    'set -l shortcuts_file "$HOME/.config/shortcuts/shortcuts.fish"\n'
                    'if test -f $shortcuts_file\n'
                    '    source $shortcuts_file\n'
                    'end\n'
                    f'# {self.marker_end}\n'
                )

                if loader.exists():
                    current = loader.read_text(encoding='utf-8')
                    if current != loader_content:
                        backup = self._backup_file(loader)
                        loader.write_text(loader_content, encoding='utf-8')
                        self.result['modified_files'].append(str(loader))
                        if backup:
                            self.result['backups'].append(str(backup))
                else:
                    loader.write_text(loader_content, encoding='utf-8')
                    self.result['created_files'].append(str(loader))

                self.result['rc_file'] = str(loader)
                self.result['user_shortcuts_file'] = str(self.user_fish_file)
                self.result['ok'] = True
                self.result['message'] = '已安装 shortcuts 载入到 fish conf.d'

            else:
                self.result['message'] = f'暂不支持的 shell：{shell_name}'
                self._print_result(self.result)
                return 2

            self._print_result(self.result)
            return 0 if self.result.get('ok') else 1

        except Exception as exc:
            self.result['ok'] = False
            self.result['message'] = f'发生错误：{exc}'
            self._print_result(self.result)
            return 1

    def _print_result(self, result: dict) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        status = '成功' if result.get('ok') else '失败'
        print(f'[shortcuts] 安装{status}')
        if result.get('message'):
            print(f'- 提示: {result["message"]}')
        if result.get('shell'):
            print(f'- shell: {result["shell"]}')
        if result.get('rc_file'):
            print(f'- 配置文件: {result["rc_file"]}')
        if result.get('user_shortcuts_file'):
            print(f'- 快捷键文件: {result["user_shortcuts_file"]}')
        created = result.get('created_files') or []
        if created:
            print('- 新建文件:')
            for p in created:
                print(f'  * {p}')
        modified = result.get('modified_files') or []
        if modified:
            print('- 修改文件:')
            for p in modified:
                print(f'  * {p}')
        backups = result.get('backups') or []
        if backups:
            print('- 已创建备份:')
            for p in backups:
                print(f'  * {p}')

    # Helpers

    def _detect_shell(self, shell: Optional[str]) -> Optional[str]:
        if shell:
            name = os.path.basename(shell).lower()
            return self._normalize_shell_name(name)
        env_shell = os.environ.get('SHELL')
        if env_shell:
            name = os.path.basename(env_shell).lower()
            return self._normalize_shell_name(name)
        return None

    def _normalize_shell_name(self, name: str) -> Optional[str]:
        if 'bash' in name:
            return 'bash'
        if 'zsh' in name:
            return 'zsh'
        if 'fish' in name:
            return 'fish'
        return None

    def _rc_file_for(self, shell_name: str) -> Path:
        home = Path.home()
        if shell_name == 'bash':
            return home / '.bashrc'
        if shell_name == 'zsh':
            return home / '.zshrc'
        raise ValueError(f'不支持的 shell: {shell_name}')

    def _ensure_block(self, rc_file: Path, block: str) -> (bool, Optional[Path]):
        content = rc_file.read_text(
            encoding='utf-8') if rc_file.exists() else ''
        if self.marker_start in content and self.marker_end in content:
            return False, None
        backup = self._backup_file(rc_file)
        # 保证换行分隔
        if content and not content.endswith('\n'):
            content += '\n'
        content += '\n' + block
        rc_file.write_text(content, encoding='utf-8')
        return True, backup

    def _backup_file(self, path: Path) -> Optional[Path]:
        try:
            if not path.exists():
                return None
            ts = datetime.now().strftime('%Y%m%d%H%M%S')
            backup = path.with_name(path.name + f'.bak-shortcuts-{ts}')
            shutil.copy2(path, backup)
            return backup
        except Exception:
            return None
