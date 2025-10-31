import sys
import time

class MemoryInfo:

    def __init__(self, rom_info_file):
        self.mem_info = self._get_rom_info(rom_info_file)
        self._cache = {}

    def eval_addr(self, addr):
        addr = addr.strip('$')
        return int(addr, 16)

    def _get_rom_info(self, rom_info_file):
        sys.stderr.write(f'Read ROM Info file: {rom_info_file.name!r}\n')
        rom_info = []
        next_update = time.time() + 0.5
        for line_no, line in enumerate(rom_info_file):
            if time.time() > next_update:
                sys.stderr.write('\rRead %i lines...' % line_no)
                sys.stderr.flush()
                next_update = time.time() + 0.5
            try:
                addr_raw, comment = line.split(';', 1)
            except ValueError:
                continue
            try:
                start_addr_raw, end_addr_raw = addr_raw.split('-')
            except ValueError:
                start_addr_raw = addr_raw
                end_addr_raw = None
            start_addr = self.eval_addr(start_addr_raw)
            if end_addr_raw:
                end_addr = self.eval_addr(end_addr_raw)
            else:
                end_addr = start_addr
            rom_info.append((start_addr, end_addr, comment.strip()))
        sys.stderr.write(f'ROM Info file: {rom_info_file.name!r} readed.\n')
        return rom_info

    def get_shortest(self, addr):
        try:
            return self._cache[addr]
        except KeyError:
            pass
        shortest = None
        size = sys.maxsize
        for start, end, txt in self.mem_info:
            if not start <= addr <= end:
                continue
            current_size = abs(end - start)
            if current_size < size:
                size = current_size
                shortest = (start, end, txt)
        if shortest is None:
            info = f'${addr:x}: UNKNOWN'
        else:
            start, end, txt = shortest
            if start == end:
                info = f'${addr:x}: {txt}'
            else:
                info = f'${addr:x}: ${start:x}-${end:x} - {txt}'
        self._cache[addr] = info
        return info