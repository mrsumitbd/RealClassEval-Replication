import ait
import csv
import os

class TlmDictWriter:
    """TlmDictWriter

    Writes telemetry dictionary to a file in selected formats
    """

    def __init__(self, tlmdict=None):
        self.tlmdict = tlmdict or getDefaultDict()

    def write_to_csv(self, output_path=None):
        """writeToCSV - write the telemetry dictionary to csv"""
        header = ['Name', 'First Byte', 'Last Byte', 'Bit Mask', 'Endian', 'Type', 'Description', 'Values']
        if output_path is None:
            output_path = ait.config._directory
        for pkt_name in self.tlmdict:
            filename = os.path.join(output_path, pkt_name + '.csv')
            with open(filename, 'wt') as output:
                csvwriter = csv.writer(output, quoting=csv.QUOTE_ALL)
                csvwriter.writerow(header)
                for fld in self.tlmdict[pkt_name].fields:
                    desc = fld.desc.replace('\n', ' ') if fld.desc is not None else ''
                    mask = hex(fld.mask) if fld.mask is not None else ''
                    enums = '\n'.join(('%s: %s' % (k, fld.enum[k]) for k in fld.enum)) if fld.enum is not None else ''
                    row = [fld.name, fld.slice().start, fld.slice().stop, mask, fld.type.endian, fld.type.name, desc, enums]
                    csvwriter.writerow(row)