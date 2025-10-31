from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(slots=True)
class CLIResult:
    '''Standard result structure for CLI commands.'''
    ok: Optional[bool] = None
    code: Optional[int] = None
    message: Optional[str] = None
    data: Any = None
    error: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    meta: dict[str, Any] = field(default_factory=dict)

    def is_success(self) -> bool:
        '''Check if the result represents success.'''
        if self.ok is True:
            return True
        if self.ok is False:
            return False
        if self.code is not None:
            return self.code == 0
        if self.error:
            return False
        if self.stderr:
            return False
        return True

    def to_dict(self) -> dict[str, Any]:
        '''Convert result to dictionary for JSON output.'''
        result: dict[str, Any] = {'success': self.is_success()}
        if self.code is not None:
            result['code'] = self.code
        if self.message is not None:
            result['message'] = self.message
        if self.data is not None:
            result['data'] = self.data
        if self.error is not None:
            result['error'] = self.error
        if self.stdout is not None:
            result['stdout'] = self.stdout
        if self.stderr is not None:
            result['stderr'] = self.stderr
        if self.meta:
            result['meta'] = self.meta
        return result
