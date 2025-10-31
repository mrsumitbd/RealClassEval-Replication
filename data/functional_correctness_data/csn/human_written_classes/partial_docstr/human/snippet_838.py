import time
import sys
import itertools

class BaseRunner:

    def __init__(self, args):
        self.args = args

    def run(self):
        """Main program entry point after parsing arguments"""
        start = time.clock()
        it = iter(self.reader)
        if self.args.max_records:
            it = itertools.islice(it, self.args.max_records)
        num = self.work(it)
        end = time.clock()
        print('Read {} records in {} seconds'.format(num, end - start), file=sys.stderr)

    def work(self, it):
        num = 0
        for num, r in enumerate(it):
            if num % 10000 == 0:
                print(num, ''.join(map(str, [r.CHROM, ':', r.POS])), sep='\t', file=sys.stderr)
            self.writer.write_record(r)
        return num