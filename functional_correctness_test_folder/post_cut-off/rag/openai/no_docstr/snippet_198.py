
import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any


class ShortcutsCommand:
    '''处理快捷键安装和管理的命令'''

    def __init__(self):
        '''初始化快捷键命令'''
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def run(self, shell: Optional[str] = None) -> int:
        '''
        安装并管理快捷键
        '''
        # 默认使用 bash
        shell = shell or 'bash'
        self.logger.info(f'开始安装快捷键，使用的 shell 为: {shell}')

        # 目标文件：~/.{shell}rc
        home = Path.home()
        rc_file = home / f'.{shell}rc'
        shortcut_file = home / '.shortcuts'

        result: Dict[str, Any] = {
            'shell': shell,
            'rc_file': str(rc_file),
            'shortcut_file': str(shortcut_file),
            'status': 'success',
            'message': '',
        }

        try:
            # 创建快捷键文件（示例内容）
            if not shortcut_file.exists():
                shortcut_file.write_text('# 这里放快捷键定义\n')
                self.logger.info(f'创建快捷键文件: {shortcut_file}')
            else:
                self.logger.info(f'快捷键文件已存在: {shortcut_file}')

            # 在 rc 文件中添加引用
            rc_content = rc_file.read_text() if rc_file.exists() else ''
            include_line = f'source {shortcut_file}\n'
            if include_line not in rc_content:
                rc_file.write_text(rc_content + include_line)
                self.logger.info(f'已在 {rc_file} 中添加 source 语句')
            else:
                self.logger.info(f'{rc_file} 已包含 source 语句')

            self._print_result(result)
            return 0
        except Exception as exc:
            result['status'] = 'error'
            result['message'] = str(exc)
            self._print_result(result)
            return 1

    def _print_result(self, result: Dict[str, Any]) -> None:
        '''
        打印操作结果
        Args:
            result: 操作结果字典
        '''
        self.logger.info('=== 快捷键安装结果 ===')
        for key, value in result.items():
            self.logger.info(f'{key}: {value}')
        self.logger.info('=== 结束 ===')
