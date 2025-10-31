from typing import Dict, List, Set, TextIO
import sys

class ContractJoiner:

    def __init__(self, import_map: Dict[str, str]=None):
        self.seen_pragmas: Set[str] = set()
        self.seen_contracts: Set[str] = set()
        self.import_map = import_map if import_map else {}

    def join(self, contract_file: TextIO) -> List[str]:
        out: List[str] = []
        if contract_file.name in self.seen_contracts:
            print('Skipping duplicate {}'.format(contract_file.name), file=sys.stderr)
            return []
        self.seen_contracts.add(contract_file.name)
        print('Reading {}'.format(contract_file.name), file=sys.stderr)
        for line in contract_file:
            line = line.strip('\r\n')
            stripped_line = line.strip()
            if stripped_line.startswith('pragma') or stripped_line.startswith('// SPDX-License-Identifier: MIT'):
                self._on_pragma_line(line=line, out=out)
            elif stripped_line.startswith('import'):
                self._on_import_line(stripped_line=stripped_line, out=out)
            else:
                out.append(line)
        return out

    def _on_pragma_line(self, line: str, out: List[str]) -> None:
        if line not in self.seen_pragmas:
            self.seen_pragmas.add(line)
            out.append(line)

    def _on_import_line(self, stripped_line: str, out: List[str]) -> None:
        match = IMPORT_RE.match(stripped_line)
        if match:
            next_file = match.groupdict().get('contract')
            assert next_file
            for prefix, path in self.import_map.items():
                if next_file.startswith(prefix):
                    next_file = next_file.replace(prefix, path)
            with open(next_file) as next_contract:
                out.extend(self.join(next_contract))