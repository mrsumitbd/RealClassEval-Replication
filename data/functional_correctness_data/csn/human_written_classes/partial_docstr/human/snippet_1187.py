import os
import math
import random
import sys
import resource

class FqMerger:
    """Class for merging several RNF FASTQ files.

        Args:
                mode (str): Output mode (single-end / paired-end-bwa / paired-end-bfast).
                input_files_fn (list): List of file names of input FASTQ files.
                output_prefix (str): Prefix for output FASTQ files.
        """

    def __init__(self, mode, input_files_fn, output_prefix):
        self.mode = mode
        self.input_files_fn = input_files_fn
        self.output_prefix = output_prefix
        self.rng = random.Random()
        self.rng.seed(1)
        files_to_be_opened_estimate = 2 + len(input_files_fn) + 10
        os_allowed_files, _ = resource.getrlimit(resource.RLIMIT_NOFILE)
        print(len(input_files_fn), files_to_be_opened_estimate, os_allowed_files)
        self.keep_files_open = os_allowed_files > files_to_be_opened_estimate
        self.i_files = [FileReader(fn, keep_file_open=self.keep_files_open) for fn in input_files_fn]
        self.i_files_sizes = [os.path.getsize(fn) for fn in input_files_fn]
        self.i_files_proc = [math.ceil(100.0 * x / sum(self.i_files_sizes)) for x in self.i_files_sizes]
        self.i_files_weighted = []
        for i in range(len(self.i_files)):
            self.i_files_weighted.extend(self.i_files_proc[i] * [self.i_files[i]])
        read_tuple_id_length_est = math.ceil(math.log(sum(self.i_files_sizes) / 20, 16))
        if mode == 'single-end':
            self.output_files_fn = ['{}.fq'.format(output_prefix)]
            self.output = FqMergerOutput(fq_1_fn=self.output_files_fn[0], reads_in_tuple=1, read_tuple_id_width=read_tuple_id_length_est)
            self._reads_in_tuple = 1
        elif mode == 'paired-end-bwa':
            self.output_files_fn = ['{}.1.fq'.format(output_prefix), '{}.2.fq'.format(output_prefix)]
            self.output = FqMergerOutput(fq_1_fn=self.output_files_fn[0], fq_2_fn=self.output_files_fn[1], reads_in_tuple=2, read_tuple_id_width=read_tuple_id_length_est)
            self._reads_in_tuple = 2
        elif mode == 'paired-end-bfast':
            self.output_files_fn = ['{}.fq'.format(output_prefix)]
            self.output = FqMergerOutput(fq_1_fn=self.output_files_fn[0], reads_in_tuple=2, read_tuple_id_width=read_tuple_id_length_est)
            self._reads_in_tuple = 2
        else:
            raise ValueError("Unknown mode '{}'".format(mode))

    def run(self):
        """Run merging.
                """
        print('', file=sys.stderr)
        print('Going to merge/convert RNF-FASTQ files.', file=sys.stderr)
        print('', file=sys.stderr)
        print('   mode:          ', self.mode, file=sys.stderr)
        print('   input files:   ', ', '.join(self.input_files_fn), file=sys.stderr)
        print('   output files:  ', ', '.join(self.output_files_fn), file=sys.stderr)
        print('', file=sys.stderr)
        while len(self.i_files_weighted) > 0:
            file_id = self.rng.randint(0, len(self.i_files_weighted) - 1)
            for i in range(READS_IN_GROUP * self._reads_in_tuple):
                if self.i_files_weighted[file_id].closed:
                    del self.i_files_weighted[file_id]
                    break
                ln1 = self.i_files_weighted[file_id].readline()
                ln2 = self.i_files_weighted[file_id].readline()
                ln3 = self.i_files_weighted[file_id].readline()
                ln4 = self.i_files_weighted[file_id].readline()
                if ln1 == '' or ln2 == '' or ln3 == '' or (ln4 == ''):
                    self.i_files_weighted[file_id].close()
                    del self.i_files_weighted[file_id]
                    break
                assert ln1[0] == '@', ln1
                assert ln3[0] == '+', ln3
                self.output.save_read(ln1, ln2, ln3, ln4)
        self.output.close()