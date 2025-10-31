import pathlib
from typing import Any, Dict, List, Optional, Set, Tuple
import re

class DriverAnalyzer:
    """
    Encapsulates driver analysis functionality with shared state.

    This class maintains pre-compiled regex patterns and file content
    to avoid duplication and improve performance.
    """

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        """
        Initialize analyzer with file contents.

        Args:
            file_contents: Dictionary mapping file paths to their content
        """
        self.file_contents = file_contents
        self.all_content = '\n'.join(file_contents.values())
        self._func_pattern_cache: Dict[str, re.Pattern] = {}
        self._access_pattern = re.compile('(write|read)([blwq]?)\\s*\\([^)]*\\b(REG_[A-Z0-9_]+)\\b')
        self._delay_pattern = re.compile('(udelay|mdelay|msleep|usleep_range)\\s*\\(\\s*(\\d+)', re.IGNORECASE)

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        """Get cached function pattern for register name."""
        if reg_name not in self._func_pattern_cache:
            self._func_pattern_cache[reg_name] = re.compile('(\\w+)\\s*\\([^)]*\\)\\s*\\{.*?' + re.escape(reg_name) + '.*?\\}', re.DOTALL)
        return self._func_pattern_cache[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        """
        Analyze the function context where a register is used.

        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        """
        context = {'function': None, 'dependencies': [], 'timing': 'unknown', 'access_pattern': 'unknown'}
        func_pattern = self._get_function_pattern(reg_name)
        content = self.all_content
        for match in re.finditer('(\\w+)\\s*\\([^)]*\\)\\s*\\{', content):
            func_name = match.group(1)
            start_pos = match.end() - 1
            brace_count = 1
            pos = start_pos + 1
            while pos < len(content) and brace_count > 0:
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1
            if brace_count == 0:
                func_body = content[start_pos:pos]
                reg_pattern = re.compile('\\b' + re.escape(reg_name) + '\\b|\\b(REG_\\w*|IWL_\\w*)\\s*\\\\\\s*\\n.*?' + re.escape(reg_name), re.MULTILINE | re.DOTALL)
                if reg_pattern.search(func_body):
                    context['function'] = func_name
                    dep_pattern = re.compile('\\b(REG_[A-Z0-9_]+)\\b')
                    deps = set(dep_pattern.findall(func_body))
                    deps.discard(reg_name)
                    context['dependencies'] = list(deps)[:5]
                    timing = self._determine_timing(func_name, func_body)
                    context['timing'] = timing
                    context['access_pattern'] = self._analyze_access_pattern(func_body, reg_name)
                    break
        return context

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        """
        Determine timing context with fallback detection.

        Args:
            func_name: Name of the function
            func_body: Content of the function

        Returns:
            Timing classification string
        """
        func_lower = func_name.lower()
        if any((keyword in func_lower for keyword in ['init', 'probe', 'start'])):
            return 'early'
        elif any((keyword in func_lower for keyword in ['exit', 'remove', 'stop'])):
            return 'late'
        elif any((keyword in func_lower for keyword in ['irq', 'interrupt', 'handler'])):
            return 'interrupt'
        if re.search('\\bprobe\\b', func_body, re.IGNORECASE):
            return 'early'
        elif re.search('\\bresume\\b', func_body, re.IGNORECASE):
            return 'runtime'
        elif re.search('\\bsuspend\\b', func_body, re.IGNORECASE):
            return 'late'
        return 'runtime'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        """Analyze register access patterns within a function."""
        write_pattern = re.compile('write[blwq]?\\s*\\([^)]*' + re.escape(reg_name), re.IGNORECASE)
        read_pattern = re.compile('read[blwq]?\\s*\\([^)]*' + re.escape(reg_name), re.IGNORECASE)
        writes = list(write_pattern.finditer(func_body))
        reads = list(read_pattern.finditer(func_body))
        write_count = len(writes)
        read_count = len(reads)
        if write_count > 0 and read_count > 0:
            if write_count == 1 and read_count == 1:
                write_pos = writes[0].start()
                read_pos = reads[0].start()
                if write_pos < read_pos:
                    return 'write_then_read'
                else:
                    return 'balanced'
            elif write_count > read_count * 1.5:
                return 'write_heavy'
            elif read_count > write_count * 1.5:
                return 'read_heavy'
            else:
                return 'balanced'
        elif write_count > 0:
            return 'write_heavy'
        elif read_count > 0:
            return 'read_heavy'
        else:
            return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str]=None) -> List[Dict[str, Any]]:
        """
        Analyze register access sequences with improved function parsing.

        Enhanced to handle nested braces properly using balance counter.
        """
        sequences = []
        content = self.all_content
        for match in re.finditer('(\\w+)\\s*\\([^)]*\\)\\s*\\{', content):
            func_name = match.group(1)
            start_pos = match.end() - 1
            brace_count = 1
            pos = start_pos + 1
            while pos < len(content) and brace_count > 0:
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1
            if brace_count == 0:
                func_body = content[start_pos:pos]
                accesses = []
                for access_match in self._access_pattern.finditer(func_body):
                    operation = access_match.group(1)
                    bit_suffix = access_match.group(2)
                    register = access_match.group(3)
                    if reg_name and register != reg_name:
                        continue
                    accesses.append((operation, register, access_match.start(), bit_suffix))
                if len(accesses) > 0:
                    for i, (op, reg, pos, bit_suffix) in enumerate(accesses):
                        sequence = {'function': func_name, 'position': i, 'total_ops': len(accesses), 'operation': op, 'register': reg, 'bit_width': BIT_WIDTH_MAP.get(bit_suffix, 32)}
                        if i > 0:
                            sequence['preceded_by'] = accesses[i - 1][1]
                            sequence['preceded_by_op'] = accesses[i - 1][0]
                        if i < len(accesses) - 1:
                            sequence['followed_by'] = accesses[i + 1][1]
                            sequence['followed_by_op'] = accesses[i + 1][0]
                        sequences.append(sequence)
        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str]=None) -> List[Dict[str, Any]]:
        """Analyze timing constraints and delays related to register accesses."""
        constraints = []
        for delay_match in self._delay_pattern.finditer(self.all_content):
            delay_type = delay_match.group(1).lower()
            delay_value = int(delay_match.group(2))
            if delay_type in ['mdelay', 'msleep']:
                delay_us = delay_value * 1000
            elif delay_type == 'udelay':
                delay_us = delay_value
            else:
                delay_us = delay_value
            context_start = max(0, delay_match.start() - 200)
            context_end = min(len(self.all_content), delay_match.end() + 200)
            context = self.all_content[context_start:context_end]
            reg_pattern = re.compile('\\b(REG_[A-Z0-9_]+)\\b')
            nearby_regs = reg_pattern.findall(context)
            if reg_name and reg_name not in nearby_regs:
                continue
            if nearby_regs:
                constraint = {'delay_us': delay_us, 'registers': list(set(nearby_regs)), 'context': 'register_access'}
                pre_context = self.all_content[context_start:delay_match.start()]
                post_context = self.all_content[delay_match.end():context_end]
                if re.search('write[blwq]?\\s*\\([^)]*', pre_context):
                    constraint['type'] = 'post_write_delay'
                elif re.search('read[blwq]?\\s*\\([^)]*', post_context):
                    constraint['type'] = 'pre_read_delay'
                else:
                    constraint['type'] = 'general_delay'
                constraints.append(constraint)
        return constraints