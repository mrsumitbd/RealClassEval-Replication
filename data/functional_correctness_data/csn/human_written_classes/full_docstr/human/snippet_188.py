from gimmemotifs.motif import read_motifs
from scipy.cluster.hierarchy import dendrogram, linkage
from gimmemotifs.utils import join_max, pfmfile_location
import seaborn as sns
import os
import pandas as pd
from matplotlib.gridspec import GridSpec
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt
import glob
import numpy as np

class MaelstromResult:
    """Class for working with maelstrom output."""

    def __init__(self, outdir):
        """Initialize a MaelstromResult object from a maelstrom output
        directory.

        Parameters
        ----------
        outdir : str
            Name of a maelstrom output directory.

        See Also
        --------
        maelstrom.run_maelstrom : Run a maelstrom analysis.
        """
        if not os.path.exists(outdir):
            raise FileNotFoundError('No such directory: ' + outdir)
        fnames = glob.glob(os.path.join(outdir, 'nonredundant*.p[fw]m'))
        if len(fnames) == 0:
            fnames = glob.glob(os.path.join(outdir, '*.p[fw]m'))
        if len(fnames) > 0:
            pfmfile = fnames[0]
            with open(pfmfile) as fin:
                self.motifs = {m.id: m for m in read_motifs(fin)}
        self.activity = {}
        for fname in glob.glob(os.path.join(outdir, 'activity*txt')):
            _, name, mtype, _, _ = os.path.split(fname)[-1].split('.')
            self.activity[f'{name}.{mtype}'] = pd.read_table(fname, comment='#', index_col=0)
        self.result = pd.read_table(os.path.join(outdir, 'final.out.txt'), comment='#', index_col=0)
        self.correlation = self.result.loc[:, self.result.columns.str.contains('corr')]
        self.percent_match = self.result.loc[:, self.result.columns.str.contains('% with motif')]
        self.result = self.result.loc[:, ~self.result.columns.str.contains('corr') & ~self.result.columns.str.contains('% with motif')]
        self.scores = pd.read_table(os.path.join(outdir, 'motif.score.txt.gz'), index_col=0)
        self.counts = pd.read_table(os.path.join(outdir, 'motif.count.txt.gz'), index_col=0)
        fname = os.path.join(outdir, 'motif.freq.txt')
        if os.path.exists(fname):
            self.freq = pd.read_table(fname, index_col=0)
        try:
            self.input = pd.read_table(os.path.join(outdir, 'input.table.txt'), index_col=0)
            if self.input.shape[1] == 1:
                self.input.columns = ['cluster']
        except Exception:
            pass

    def plot_heatmap(self, kind='final', min_freq=0.01, threshold=2, name=True, indirect=True, figsize=None, max_number_factors=5, aspect=1, cmap='RdBu_r', **kwargs):
        """Plot clustered heatmap of predicted motif activity.

        Parameters
        ----------
        kind : str, optional
            Which data type to use for plotting. Default is 'final', which will
            plot the result of the rank aggregation. Other options are 'freq'
            for the motif frequencies, or any of the individual activities such
            as 'rf.score'.

        min_freq : float, optional
            Minimum frequency of motif occurrence.

        threshold : float, optional
            Minimum activity (absolute) of the rank aggregation result.

        name : bool, optional
            Use factor names instead of motif names for plotting.

        indirect : bool, optional
            Include indirect factors (computationally predicted or non-curated). Default is True.

        max_number_factors : int, optional
            Truncate the list of factors to this maximum size.

        figsize : tuple, optional
            Tuple of figure size (width, height).

        aspect : int, optional
            Aspect ratio for tweaking the plot.

        cmap : str, optional
            Color paletter to use, RdBu_r by default.

        kwargs : other keyword arguments
            All other keyword arguments are passed to sns.heatmap

        Returns
        -------
        cg : ClusterGrid
            A seaborn ClusterGrid instance.
        """
        filt = np.any(np.abs(self.result) >= threshold, 1)
        if hasattr(self, 'freq'):
            filt = filt & np.any(np.abs(self.freq.T) >= min_freq, 1)
        else:
            filt = filt & (self.counts.sum() / self.counts.shape[0] > min_freq)
        idx = self.result.loc[filt].index
        if idx.shape[0] == 0:
            logger.warning('Empty matrix, try lowering the threshold')
            return
        if idx.shape[0] >= 100:
            logger.warning('The filtered matrix has more than 100 rows.')
            logger.warning('It might be worthwhile to increase the threshold for visualization')
        if kind == 'final':
            data = self.result
        elif kind == 'freq':
            if hasattr(self, 'freq'):
                data = self.freq.T
                cmap = 'Reds'
            else:
                raise ValueError('frequency plot only works with maelstrom output from clusters')
        elif kind in self.activity:
            data = self.activity[kind]
            if kind in ['hypergeom.count', 'mwu.score']:
                cmap = 'Reds'
        else:
            raise ValueError('Unknown dtype')
        m = data.loc[idx]
        if 'vmax' in kwargs:
            vmax = kwargs.pop('vmax')
        else:
            vmax = max(abs(np.percentile(m, 1)), np.percentile(m, 99))
        if 'vmin' in kwargs:
            vmin = kwargs.pop('vmin')
        else:
            vmin = -vmax
        if name:
            m['factors'] = [self.motifs[n].format_factors(max_length=max_number_factors, html=False, include_indirect=indirect, extra_str=',..') for n in m.index]
            m = m.set_index('factors')
        h, w = m.shape
        if figsize is None:
            figsize = (4 + m.shape[1] / 4, 1 + m.shape[0] / 3)
        fig = plt.figure(figsize=figsize)
        npixels = 30
        g = GridSpec(2, 1, height_ratios=(fig.get_figheight() * fig.dpi - npixels, npixels))
        ax1 = fig.add_subplot(g[0, :])
        ax2 = fig.add_subplot(g[1, :])
        ax2.set_title('aggregated z-score')
        dm = pdist(m, metric='correlation')
        hc = linkage(dm, method='ward')
        leaves = dendrogram(hc, no_plot=True)['leaves']
        cg = sns.heatmap(m.iloc[leaves], ax=ax1, cbar_ax=ax2, cbar_kws={'orientation': 'horizontal'}, cmap=cmap, linewidths=1, vmin=vmin, vmax=vmax, **kwargs)
        plt.setp(cg.axes.xaxis.get_majorticklabels(), rotation=90)
        plt.tight_layout()
        return cg

    def plot_scores(self, motifs, name=True, max_len=50):
        """Create motif scores boxplot of different clusters.
        Motifs can be specified as either motif or factor names.
        The motif scores will be scaled and plotted as z-scores.

        Parameters
        ----------
        motifs : iterable or str
            List of motif or factor names.

        name : bool, optional
            Use factor names instead of motif names for plotting.

        max_len : int, optional
            Truncate the list of factors to this maximum length.

        Returns
        -------

        g : FacetGrid
            Returns the seaborn FacetGrid object with the plot.
        """
        if self.input.shape[1] != 1:
            raise ValueError("Can't make a categorical plot with real-valued data")
        if type('') == type(motifs):
            motifs = [motifs]
        plot_motifs = []
        for motif in motifs:
            if motif in self.motifs:
                plot_motifs.append(motif)
            else:
                for m in self.motifs.values():
                    if motif in m.factors:
                        plot_motifs.append(m.id)
        data = self.scores[plot_motifs]
        data[:] = data.scale(data, axix=0)
        if name:
            data = data.T
            data['factors'] = [join_max(self.motifs[n].factors, max_len, ',', suffix=',(...)') for n in plot_motifs]
            data = data.set_index('factors').T
        data = pd.melt(self.input.join(data), id_vars=['cluster'])
        data.columns = ['cluster', 'motif', 'z-score']
        g = sns.catplot(data=data, y='motif', x='z-score', hue='cluster', kind='box', aspect=2)
        return g