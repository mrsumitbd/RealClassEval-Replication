
from dataclasses import dataclass
import json
import os


@dataclass
class MultiSearchResult:

    def __str__(self) -> str:
        return str(self.__dict__)

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        return '\n'.join([result.to_json() for result in results])

    @classmethod
    def to_string(cls, results: list['MultiSearchResult']) -> str:
        return '\n'.join([str(result) for result in results])

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        return os.path.relpath(file_path, source_path)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.java': 'Java',
            '.c': 'C',
            '.cpp': 'C++',
            '.h': 'C/C++ Header',
            '.hpp': 'C++ Header',
            '.cs': 'C#',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.rs': 'Rust',
            '.scala': 'Scala',
            '.ts': 'TypeScript',
            '.m': 'Objective-C',
            '.mm': 'Objective-C++',
            '.r': 'R',
            '.pl': 'Perl',
            '.lua': 'Lua',
            '.sh': 'Shell',
            '.bash': 'Bash',
            '.ps1': 'PowerShell',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.md': 'Markdown',
            '.txt': 'Text',
            '.csv': 'CSV',
            '.sql': 'SQL',
            '.gitignore': 'Git Ignore',
            '.dockerignore': 'Docker Ignore',
            '.env': 'Environment',
            '.ini': 'INI',
            '.toml': 'TOML',
            '.lock': 'Lock',
            '.log': 'Log',
            '.pdf': 'PDF',
            '.jpg': 'JPEG',
            '.jpeg': 'JPEG',
            '.png': 'PNG',
            '.gif': 'GIF',
            '.bmp': 'BMP',
            '.svg': 'SVG',
            '.mp3': 'MP3',
            '.wav': 'WAV',
            '.mp4': 'MP4',
            '.avi': 'AVI',
            '.mkv': 'MKV',
            '.zip': 'ZIP',
            '.tar': 'TAR',
            '.gz': 'GZ',
            '.rar': 'RAR',
            '.7z': '7Z',
            '.exe': 'EXE',
            '.dll': 'DLL',
            '.so': 'SO',
            '.a': 'A',
            '.lib': 'LIB',
            '.obj': 'OBJ',
            '.o': 'O',
            '.class': 'Class',
            '.jar': 'JAR',
            '.war': 'WAR',
            '.ear': 'EAR',
            '.apk': 'APK',
            '.ipa': 'IPA',
            '.dmg': 'DMG',
            '.iso': 'ISO',
            '.bin': 'BIN',
            '.img': 'IMG',
            '.vmdk': 'VMDK',
            '.vdi': 'VDI',
            '.vhd': 'VHD',
            '.vhdx': 'VHDX',
            '.qcow2': 'QCOW2',
            '.ova': 'OVA',
            '.ovf': 'OVF',
            '.vbox': 'VBOX',
            '.vmx': 'VMX',
            '.vmsd': 'VMSD',
            '.vmss': 'VMSS',
            '.vmtm': 'VMTM',
            '.nvram': 'NVRAM',
            '.vmem': 'VMEM',
            '.vmsn': 'VMSN',
            '.vmxf': 'VMXF',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vmx': 'VMX',
            '.vm
