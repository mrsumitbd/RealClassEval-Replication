import sys
import time

class XroarTraceInfo:

    def __init__(self, infile, outfile, add_cc):
        self.infile = infile
        self.outfile = outfile
        self.add_cc = add_cc

    def add_info(self, rom_info):
        last_line_no = 0
        next_update = time.time() + 1
        for line_no, line in enumerate(self.infile):
            if time.time() > next_update:
                sys.stderr.write('\rRead %i lines (%i/sec.)...' % (line_no, line_no - last_line_no))
                sys.stderr.flush()
                last_line_no = line_no
                next_update = time.time() + 1
            addr = line[:4]
            try:
                addr = int(addr, 16)
            except ValueError:
                self.outfile.write(line)
                continue
            line = line.strip()
            if self.add_cc:
                cc = line[49:51]
                if cc:
                    try:
                        cc = int(cc, 16)
                    except ValueError as err:
                        msg = f'ValueError: {err} in line: {line}'
                        line += f'| {msg}'
                    else:
                        cc_info = cc_value2txt(cc)
                        line += '| ' + cc_info
            addr_info = rom_info.get_shortest(addr)
            self.outfile.write(f'{line} | {addr_info}\n')