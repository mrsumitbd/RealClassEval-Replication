from typing import Optional, Union, List, Any
import scipy.linalg
import pandas as pd
import numpy as np

class DiscreteMarkovModelSim:
    """Simulate a discrete n-state character on a phylogenetic tree.

    Input Q matrix (instantaneous transition rate matrix) can be 
    estimated from tip states using DiscreteMarkovModelFit.

    Parameters
    ----------
    tree
        ...
    qmatrix
        ...
    nsims
        ...

    Examples
    --------
    >>> import toytree
    >>> tree = toytree.rtree.unittree(10)
    >>> qmatrix = [[-0.7, 0.3], [0.5, -0.5]]
    >>> data = tree.pcm.simulate_discrete_markov_model(qmatrix, nsims=100)

    See also:
    ---------
    ...

    References:
    -----------
    ...
    """

    def __init__(self, tree: 'toytree.ToyTree', qmatrix: Union[np.ndarray, pd.DataFrame], nsims: int=1, ancestral_state: Optional[Any]=None, seed: int=None):
        self.rng = np.random.default_rng(seed)
        self.nsims = nsims
        self.tree = tree
        self.qmatrix = np.array(qmatrix)
        self.nstates = self.qmatrix.shape[0]
        self.ancestral_state = ancestral_state if ancestral_state is not None else self.rng.choice(range(self.nstates), size=nsims)
        assert self.nstates >= 2, 'discrete model must have >1 states'
        assert self.ancestral_state.size == self.nsims, 'ancestral_state must be length nsims (set for every sim'
        assert np.allclose(self.qmatrix.sum(axis=1), 0), f'rows of the Q matrix must sum to zero: {self.qmatrix.sum(axis=1)}'

    def _get_state_array(self) -> np.ndarray:
        """
        Rates are returned in units of changes per unit branch length, 
        and so should be interpreted in the context of whether blens
        are in units of years, mya, substitutions, etc.
        """
        data = np.zeros((self.nsims, self.tree.ntips), dtype=int)
        for sim in range(self.nsims):
            trait = {self.tree.treenode.idx: self.ancestral_state[sim]}
            for node in self.tree.treenode.traverse():
                if not node.is_root():
                    prob_mat = scipy.linalg.expm(node.dist * self.qmatrix)
                    trait[node.idx] = np.argmax(np.random.multinomial(1, prob_mat[trait[node.up.idx]]))
            data[sim] = [trait[i] for i in range(self.tree.ntips)]
        return data

    def _get_state_tree(self) -> List['toytree.ToyTree']:
        """
        Rates are returned in units of changes per unit branch length, 
        and so should be interpreted in the context of whether blens
        are in units of years, mya, substitutions, etc.
        """
        data = []
        for sim in range(self.nsims):
            trait = {self.tree.treenode.idx: self.ancestral_state[sim]}
            for node in self.tree.treenode.traverse():
                if not node.is_root():
                    prob_mat = scipy.linalg.expm(node.dist * self.qmatrix)
                    trait[node.idx] = np.argmax(np.random.multinomial(1, prob_mat[trait[node.up.idx]]))
            ntre = self.tree.set_node_data(feature='discrete', mapping=trait)
            data.append(ntre)
        return data