import re
import pathlib
from typing import Dict, Any, Optional, List, Tuple, Iterable


class DriverAnalyzer:

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        self.file_contents: Dict[pathlib.Path, str] = file_contents
        self._functions_cache: Dict[pathlib.Path, List[Dict[str, Any]]] = {}
        for path, text in self.file_contents.items():
            self._functions_cache[path] = list(
                self._parse_file_functions(text))

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        # Function signature pattern (C-like), does not include reg_name because we filter after extraction
        # Group 1: return type and qualifiers, Group 2: function name
        pat = r"""
            (?P<ret>\b[a-zA-Z_][\w\s\*\(\),\[\]]*)
            \s+
            (?P<name>[a-zA-Z_]\w*)
            \s*
            \(
                (?P<args>[^;{}()]|\([^()]*\))*
            \)
            \s*
            \{
        """
        return re.compile(pat, re.VERBOSE | re.MULTILINE)

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []
        for path, funcs in self._functions_cache.items():
            for f in funcs:
                body = f["body"]
                if reg_name in body:
                    timing = self._determine_timing(f["name"], body)
                    access = self._analyze_access_pattern(body, reg_name)
                    occs = list(self._find_occurrence_lines(
                        self.file_contents[path], f["body_span"][0], reg_name))
                    results.append({
                        "file": str(path),
                        "function": f["name"],
                        "signature": f["signature"],
                        "start_line": f["start_line"],
                        "end_line": f["end_line"],
                        "reg_name": reg_name,
                        "occurrence_count": len(occs),
                        "occurrence_lines": occs,
                        "access_pattern": access,
                        "timing_summary": timing,
                    })
        return {
            "query_reg": reg_name,
            "matches": results,
            "total_functions_with_reg": len(results),
        }

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        calls = self._extract_timing_calls(func_body)
        if not calls:
            return "no-explicit-delay"
        summary_parts = []
        for c in calls:
            if c["value"] is not None:
                summary_parts.append(f"{c['api']}({c['value']}{c['units']})")
            else:
                summary_parts.append(f"{c['api']}(...)")
        return ", ".join(summary_parts)

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        lines = [ln.strip() for ln in func_body.splitlines()]
        related = [ln for ln in lines if reg_name in ln]
        if not related:
            return "none"
        # Simple heuristics for common patterns
        rw_calls = self._extract_rw_calls(related, reg_name)
        has_read = any(c["type"] == "read" for c in rw_calls)
        has_write = any(c["type"] == "write" for c in rw_calls)
        writes = [c for c in rw_calls if c["type"] == "write"]
        reads = [c for c in rw_calls if c["type"] == "read"]

        if has_read and has_write:
            # Check order
            first_rw_types = [c["type"] for c in rw_calls[:4]]
            if first_rw_types[:2] == ["read", "write"]:
                # Check for read-modify-write pattern
                if self._looks_like_rmw(related, reg_name):
                    return "read-modify-write"
                return "read-then-write"
            if first_rw_types[:2] == ["write", "read"]:
                return "write-then-read"
            return "mixed-read-write"
        if has_write and not has_read:
            if len(writes) > 1:
                return "multiple-writes"
            return "write-only"
        if has_read and not has_write:
            if len(reads) > 1:
                return "multiple-reads"
            return "read-only"
        # Fall back to assignment check
        if any(re.search(rf"\b{re.escape(reg_name)}\b\s*=", ln) for ln in related):
            return "assignment-write"
        return "unknown"

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for path, funcs in self._functions_cache.items():
            for f in funcs:
                body = f["body"]
                if reg_name is not None and reg_name not in body:
                    continue
                patterns = {}
                if reg_name is None:
                    # Attempt to infer register tokens by common access helpers
                    candidates = self._infer_register_identifiers(body)
                    for rn in sorted(candidates):
                        patterns[rn] = self._analyze_access_pattern(body, rn)
                else:
                    patterns[reg_name] = self._analyze_access_pattern(
                        body, reg_name)
                if not patterns:
                    continue
                results.append({
                    "file": str(path),
                    "function": f["name"],
                    "start_line": f["start_line"],
                    "end_line": f["end_line"],
                    "patterns": patterns
                })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for path, funcs in self._functions_cache.items():
            for f in funcs:
                body = f["body"]
                if reg_name is not None and reg_name not in body:
                    continue
                calls = self._extract_timing_calls(body)
                if not calls:
                    continue
                results.append({
                    "file": str(path),
                    "function": f["name"],
                    "start_line": f["start_line"],
                    "end_line": f["end_line"],
                    "timing_calls": calls,
                    "summary": self._determine_timing(f["name"], body),
                })
        return results

    # Internal helpers

    def _parse_file_functions(self, text: str) -> Iterable[Dict[str, Any]]:
        pattern = self._get_function_pattern(reg_name="")
        for m in pattern.finditer(text):
            name = m.group("name")
            sig_start = m.start()
            body_start = m.end() - 1  # points at '{'
            body_end = self._match_brace_end(text, body_start)
            if body_end is None:
                continue
            body = text[body_start + 1:body_end]
            signature = text[sig_start:body_start].strip()
            start_line = text.count("\n", 0, sig_start) + 1
            end_line = text.count("\n", 0, body_end) + 1
            yield {
                "name": name,
                "signature": signature,
                "body": body,
                "body_span": (body_start + 1, body_end),
                "start_line": start_line,
                "end_line": end_line,
            }

    def _match_brace_end(self, text: str, open_brace_pos: int) -> Optional[int]:
        depth = 0
        i = open_brace_pos
        n = len(text)
        in_squote = False
        in_dquote = False
        in_sl_comment = False
        in_ml_comment = False
        while i < n:
            ch = text[i]
            nxt = text[i + 1] if i + 1 < n else ""
            if in_sl_comment:
                if ch == "\n":
                    in_sl_comment = False
            elif in_ml_comment:
                if ch == "*" and nxt == "/":
                    in_ml_comment = False
                    i += 1
            elif in_squote:
                if ch == "\\":
                    i += 1
                elif ch == "'":
                    in_squote = False
            elif in_dquote:
                if ch == "\\":
                    i += 1
                elif ch == '"':
                    in_dquote = False
            else:
                if ch == "/" and nxt == "/":
                    in_sl_comment = True
                    i += 1
                elif ch == "/" and nxt == "*":
                    in_ml_comment = True
                    i += 1
                elif ch == "'":
                    in_squote = True
                elif ch == '"':
                    in_dquote = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        return i
            i += 1
        return None

    def _find_occurrence_lines(self, full_text: str, body_start_pos: int, token: str) -> Iterable[int]:
        # Convert positions to line numbers for occurrences within body
        prefix_line = full_text.count("\n", 0, body_start_pos) + 1
        body_text = full_text[body_start_pos:]
        for m in re.finditer(re.escape(token), body_text):
            pos = body_start_pos + m.start()
            line_no = full_text.count("\n", 0, pos) + 1
            yield line_no

    def _extract_rw_calls(self, lines: List[str], reg_name: str) -> List[Dict[str, Any]]:
        rw_list: List[Dict[str, Any]] = []
        read_funcs = [
            "readl", "readw", "readb", "ioread32", "ioread16", "ioread8",
            "regmap_read", "i2c_smbus_read", "spi_w8r8", "spi_w8r16",
        ]
        write_funcs = [
            "writel", "writew", "writeb", "iowrite32", "iowrite16", "iowrite8",
            "regmap_write", "i2c_smbus_write", "spi_write",
        ]
        for ln in lines:
            if reg_name not in ln:
                continue
            for fn in read_funcs:
                if re.search(rf"\b{fn}\b", ln):
                    rw_list.append({"type": "read", "api": fn, "line": ln})
                    break
            else:
                for fn in write_funcs:
                    if re.search(rf"\b{fn}\b", ln):
                        rw_list.append(
                            {"type": "write", "api": fn, "line": ln})
                        break
        return rw_list

    def _looks_like_rmw(self, lines: List[str], reg_name: str) -> bool:
        # Heuristic RMW: read of reg into var, var modified with bitwise ops, then write var to reg
        assign_read = re.compile(
            rf"(\w+)\s*=\s*.*\b{re.escape(reg_name)}\b.*;")
        write_back = re.compile(
            rf"\b.*\b{re.escape(reg_name)}\b.*[,=]\s*(\w+)\s*[\);]")
        bitops = re.compile(r"\b(\w+)\s*=\s*\1\s*([|&^]|<<|>>)")
        var = None
        for ln in lines:
            m = assign_read.search(ln)
            if m:
                var = m.group(1)
            if var and bitops.search(ln):
                pass
            if var:
                wb = write_back.search(ln)
                if wb and wb.group(1) == var:
                    return True
        # Alternate pattern: read helper returning value used in write with masks
        if any(re.search(rf"\b(read\w*)\s*\([^;]*\b{re.escape(reg_name)}\b", ln) for ln in lines) and \
           any(re.search(rf"\b(write\w*)\s*\([^;]*\b{re.escape(reg_name)}\b", ln) for ln in lines):
            if any(re.search(r"[|&^]", ln) for ln in lines):
                return True
        return False

    def _infer_register_identifiers(self, body: str) -> List[str]:
        # Look for arguments to read/write helpers that look like register identifiers
        rw_helpers = r"(?:readl|readw|readb|ioread32|ioread16|ioread8|regmap_read|writel|writew|writeb|iowrite32|iowrite16|iowrite8|regmap_write)"
        regs: set = set()
        for m in re.finditer(rf"\b{rw_helpers}\s*\(([^;)]*)\)", body):
            args = m.group(1)
            # Split by comma, take tokens that look like identifiers or member accesses
            for tok in [a.strip() for a in args.split(",")]:
                if re.match(r"^[A-Za-z_]\w*(?:->\w+|\.\w+|\[\w+\])*$", tok):
                    # Prefer the first argument as potential register in many helpers
                    regs.add(tok)
        # Also capture defines like SOME_REG or REG_XXX
        for m in re.finditer(r"\b([A-Z][A-Z0-9_]{2,})\b", body):
            if "REG" in m.group(1):
                regs.add(m.group(1))
        return list(regs)

    def _extract_timing_calls(self, body: str) -> List[Dict[str, Any]]:
        timing_apis = {
            "udelay": "us",
            "ndelay": "ns",
            "mdelay": "ms",
            "usleep_range": "us",
            "usleep": "us",
            "msleep": "ms",
            "fsleep": "us",
            "schedule_timeout": "jiffies",
            "msleep_interruptible": "ms",
            "usleep_range_state": "us",
        }
        calls: List[Dict[str, Any]] = []
        for api, unit in timing_apis.items():
            for m in re.finditer(rf"\b{api}\s*\(([^)]*)\)", body):
                args = m.group(1).strip()
                val = None
                # Try to extract numeric literal
                num = re.match(r"\s*(\d+)", args)
                if num:
                    try:
                        val = int(num.group(1))
                    except ValueError:
                        val = None
                calls.append({"api": api, "value": val,
                             "units": unit, "args": args})
        return calls
