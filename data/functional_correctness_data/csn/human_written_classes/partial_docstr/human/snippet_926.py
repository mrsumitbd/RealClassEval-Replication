from ipyrad.assemble.names_to_fastqs import get_fastq_tuples_dict_from_paths_list, get_paths_list_from_fastq_str
from ipyrad.core.sample import Sample
from ipyrad.assemble.utils import IPyradError, ambigcutters, BADCHARS
import numpy as np
import os
import time
import glob

class FileLinker:
    """
    Loads Samples from file names and check sample names for bad chars.
    """

    def __init__(self, step):
        self.data = step.data
        self.input = step.sfiles
        self.fastqs = glob.glob(self.input)
        self.paired = 'pair' in self.data.params.datatype
        self.ftuples = []
        self.ipyclient = step.ipyclient
        self.lbview = self.ipyclient.load_balanced_view()

    def run(self):
        self.check_files()
        self.remote_run_linker()

    def check_files(self):
        if any([i.endswith('.bz2') for i in self.fastqs]):
            raise IPyradError(NO_SUPPORT_FOR_BZ2.format(self.input))
        endings = ('gz', 'fastq', 'fq')
        self.fastqs = [i for i in self.fastqs if i.split('.')[-1] in endings]
        if not self.fastqs:
            raise IPyradError(NO_FILES_FOUND_PAIRS.format(self.data.params.sorted_fastq_path))
        if 'pair' in self.data.params.datatype:
            if len(self.fastqs) % 2:
                raise IPyradError(PE_ODD_NUMBER_OF_FILES)
        paths = get_paths_list_from_fastq_str(self.fastqs)
        self.ftuples = get_fastq_tuples_dict_from_paths_list(paths, self.paired)

    def remote_run_linker(self):
        """read in fastq files and count nreads for stats and chunking in s2."""
        createdinc = 0
        for sname, ftup in self.ftuples.items():
            if sname not in self.data.samples:
                newsamp = Sample(sname)
                newsamp.stats.state = 1
                newsamp.barcode = None
                newsamp.files.fastqs = [(str(ftup[0]), str(ftup[1]))]
                self.data.samples[sname] = newsamp
                createdinc += 1
        rasyncs = {}
        if createdinc:
            for sample in self.data.samples.values():
                gzipped = bool(sample.files.fastqs[0][0].endswith('.gz'))
                rasyncs[sample.name] = self.lbview.apply(zbufcountlines, *(sample.files.fastqs[0][0], gzipped))
        start = time.time()
        printstr = ('loading reads       ', 's1')
        while 1:
            fin = [i.ready() for i in rasyncs.values()]
            self.data._progressbar(len(fin), sum(fin), start, printstr)
            time.sleep(0.1)
            if len(fin) == sum(fin):
                self.data._print('')
                break
        for sname in rasyncs:
            res = rasyncs[sname].get() / 4
            self.data.samples[sname].stats.reads_raw = res
            self.data.samples[sname].stats_dfs.s1['reads_raw'] = res
            self.data.samples[sname].state = 1
        if createdinc:
            if 'pair' in self.data.params.datatype:
                createdinc = createdinc * 2
            if self.data._cli:
                self.data._print('{} fastq files loaded to {} Samples.'.format(createdinc, len(self.data.samples)))
        self.data.stats_dfs.s1 = self.data._build_stat('s1')
        self.data.stats_files.s1 = os.path.join(self.data.params.project_dir, self.data.name + '_s1_demultiplex_stats.txt')
        with open(self.data.stats_files.s1, 'w') as outfile:
            self.data.stats_dfs.s1.fillna(value=0).astype(np.int64).to_string(outfile)