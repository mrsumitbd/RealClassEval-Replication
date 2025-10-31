from typing import Callable, Dict, List, Optional, Set, Tuple, Type

class SharedMemoryAllocator:

    def __init__(self) -> None:
        self.free_slots: List[Tuple[int, int]] = [(0, (1 << 32) - 1)]
        self.addr2nbytes: Dict[int, int] = {}
        self.allocated: int = 0
        self.maximum_allocated: int = 0

    def allocate(self, nbytes: int) -> int:
        nbytes = (nbytes + 127) // 128 * 128
        i = min((i for i, (start, end) in enumerate(self.free_slots) if end - start >= nbytes))
        addr = self.free_slots[i][0]
        if self.free_slots[i][1] - self.free_slots[i][0] == nbytes:
            del self.free_slots[i]
        else:
            self.free_slots[i] = (addr + nbytes, self.free_slots[i][1])
        self.addr2nbytes[addr] = nbytes
        self.maximum_allocated = max(self.maximum_allocated, addr + nbytes)
        self.allocated += nbytes
        return addr

    def free(self, addr: int) -> None:
        before = [i for i, slot in enumerate(self.free_slots) if slot[1] <= addr]
        after = [i for i, slot in enumerate(self.free_slots) if slot[0] > addr]
        assert len(before) + len(after) == len(self.free_slots)
        nbytes = self.addr2nbytes[addr]
        if before and after and (self.free_slots[before[-1]][1] == addr) and (self.free_slots[after[0]][0] == addr + nbytes):
            self.free_slots[before[-1]] = (self.free_slots[before[-1]][0], self.free_slots[after[0]][1])
        elif before and self.free_slots[before[-1]][1] == addr:
            self.free_slots[before[-1]] = (self.free_slots[before[-1]][0], addr + nbytes)
        elif after and self.free_slots[after[0]][0] == addr + nbytes:
            self.free_slots[after[0]] = (addr, self.free_slots[after[0]][1])
        else:
            self.free_slots.append((addr, addr + nbytes))
            self.free_slots = list(sorted(self.free_slots, key=lambda x: x[0]))
        self.allocated -= nbytes
        del self.addr2nbytes[addr]