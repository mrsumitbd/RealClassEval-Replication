import rnftools.rnfformat
import os

class FqMergerOutput:
    """Class for output of FqMerger.

        Args:
                reads_in_tuple (int): Number of reads in a tuple.
                fq_1_fn (str): File name of first output FASTQ.
                fq_2_fn (str): File name of second output FASTQ.
                read_tuple_id_width: Width of Read ID.
        """

    def __init__(self, reads_in_tuple, fq_1_fn, fq_2_fn=None, read_tuple_id_width=6):
        self.reads_in_tuple = reads_in_tuple
        self.fs = [open(fq_1_fn, 'w+')]
        if fq_2_fn is not None:
            self.fs.append(open(fq_2_fn, 'w+'))
        self.read_tuple_counter = 1
        self.rnf_profile = rnftools.rnfformat.RnfProfile(read_tuple_id_width=read_tuple_id_width)

    def __del__(self):
        for f in self.fs:
            if not f.closed:
                f.close()

    def close(self):
        for f in self.fs:
            f.close()

    def save_read(self, ln1, ln2, ln3, ln4):
        [ln1, ln2, ln3, ln4] = [ln1.strip(), ln2.strip(), ln3.strip(), ln4.strip()]
        ln1 = self.rnf_profile.apply(read_tuple_name=ln1, read_tuple_id=self.read_tuple_counter)
        if self.reads_in_tuple == 1:
            file_id = 0
            if ln1[-2] == '/':
                raise ValueError("Wrong read name '{}'. Single end read should not contain '/'.".format(ln1[1:]))
            self.read_tuple_counter += 1
        else:
            if ln1[-2] != '/':
                raise ValueError("Wrong read name '{}'. A read with two ends should contain '/'.".format(ln1[1:]))
            if len(self.fs) == 1:
                ln1 = ln1[:-2]
                file_id = 0
                self.read_tuple_counter += 1
            elif ln1[-1] == '1':
                file_id = 0
            elif ln1[-1] == '2':
                file_id = 1
                self.read_tuple_counter += 1
            else:
                raise ValueError("Wrong read name '{}'.".format(ln1[1:]))
        self.fs[file_id].write(''.join([ln1, os.linesep, ln2, os.linesep, ln3, os.linesep, ln4, os.linesep]))