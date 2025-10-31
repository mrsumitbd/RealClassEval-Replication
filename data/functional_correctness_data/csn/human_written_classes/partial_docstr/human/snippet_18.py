from cpplint import _cpplint_state
from typing import TextIO
import cpplint

class Lint:

    def __init__(self) -> None:
        self.project_name = 'xgboost'
        self.cpp_header_map: dict[str, dict[str, int]] = {}
        self.cpp_src_map: dict[str, dict[str, int]] = {}
        self.pylint_cats = set(['error', 'warning', 'convention', 'refactor'])
        cpplint_args = ['--quiet', '--extensions=' + ','.join(CXX_SUFFIX), '.']
        _ = cpplint.ParseArguments(cpplint_args)
        cpplint._SetFilters(','.join(['-build/c++11', '-build/include,', '+build/namespaces', '+build/include_what_you_use', '+build/include_order']))
        cpplint._SetCountingStyle('toplevel')
        cpplint._line_length = 100

    def process_cpp(self, path: str, suffix: str) -> None:
        """Process a cpp file."""
        _cpplint_state.ResetErrorCounts()
        cpplint.ProcessFile(str(path), _cpplint_state.verbose_level)
        _cpplint_state.PrintErrorCounts()
        errors = _cpplint_state.errors_by_category.copy()
        if suffix == 'h':
            self.cpp_header_map[str(path)] = errors
        else:
            self.cpp_src_map[str(path)] = errors

    @staticmethod
    def _print_summary_map(strm: TextIO, result_map: dict[str, dict[str, int]], ftype: str) -> int:
        """Print summary of certain result map."""
        if len(result_map) == 0:
            return 0
        npass = sum((1 for x in result_map.values() if len(x) == 0))
        strm.write(f'====={npass}/{len(result_map)} {ftype} files passed check=====\n')
        for fname, emap in result_map.items():
            if len(emap) == 0:
                continue
            strm.write(f'{fname}: {sum(emap.values())} Errors of {len(emap)} Categories map={str(emap)}\n')
        return len(result_map) - npass

    def print_summary(self, strm: TextIO) -> int:
        """Print summary of lint."""
        nerr = 0
        nerr += Lint._print_summary_map(strm, self.cpp_header_map, 'cpp-header')
        nerr += Lint._print_summary_map(strm, self.cpp_src_map, 'cpp-source')
        if nerr == 0:
            strm.write('All passed!\n')
        else:
            strm.write(f'{nerr} files failed lint\n')
        return nerr