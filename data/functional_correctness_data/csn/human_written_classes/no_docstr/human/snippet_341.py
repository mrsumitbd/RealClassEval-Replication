import csv

class AmberWriter:

    def __init__(self, out_handle):
        self.writer = csv.writer(out_handle, delimiter='\t')

    def write_header(self):
        self.writer.writerow(['Chromosome', 'Position', 'TumorBAF', 'TumorModifiedBAF', 'TumorDepth', 'NormalBAF', 'NormalModifiedBAF', 'NormalDepth'])

    def write_row(self, rec, stats):
        if stats['normal']['freq'] is not None and stats['normal']['depth'] is not None:
            self.writer.writerow([rec.chrom, rec.pos, stats['tumor']['freq'], _normalize_baf(stats['tumor']['freq']), stats['tumor']['depth'], stats['normal']['freq'], _normalize_baf(stats['normal']['freq']), stats['normal']['depth']])