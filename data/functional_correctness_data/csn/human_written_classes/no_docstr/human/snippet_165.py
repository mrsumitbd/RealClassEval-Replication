import numpy as np
from typing import Optional, Union, Callable, List, TYPE_CHECKING, Any, Tuple, cast
from graphistry.plugins_types.embed_types import XSymbolic, ProtoSymbolic, TT
from graphistry.utils.lazy_import import lazy_embed_import

class SubgraphIterator:

    def __init__(self, g, sample_size: int=3000, num_steps: int=1000):
        self.num_steps = num_steps
        self.sample_size = sample_size
        self.eids = np.arange(g.num_edges())
        self.g = g
        self.num_nodes = g.num_nodes()

    def __len__(self) -> int:
        return self.num_steps

    def __getitem__(self, i: int):
        _, torch, nn, dgl, GraphDataLoader, _, F, _ = lazy_embed_import()
        eids = torch.from_numpy(np.random.choice(self.eids, self.sample_size))
        src, dst = self.g.find_edges(eids)
        rel = self.g.edata[dgl.ETYPE][eids].numpy()
        triplets = np.stack((src, rel, dst)).T
        samples, labels = SubgraphIterator._sample_neg(triplets, self.num_nodes)
        src, rel, dst = samples.T
        sub_g = dgl.graph((src, dst), num_nodes=self.num_nodes)
        sub_g.edata[dgl.ETYPE] = rel
        sub_g.edata['norm'] = dgl.norm_by_dst(sub_g).unsqueeze(-1)
        return (sub_g, samples, labels)

    @staticmethod
    def _sample_neg(triplets: np.ndarray, num_nodes: int) -> Tuple[TT, TT]:
        _, torch, _, _, _, _, _, _ = lazy_embed_import()
        triplets = torch.tensor(triplets)
        h, r, t = triplets.T
        h_o_t = torch.randint(high=2, size=h.size())
        random_h = torch.randint(high=num_nodes, size=h.size())
        random_t = torch.randint(high=num_nodes, size=h.size())
        neg_h = torch.where(h_o_t == 0, random_h, h)
        neg_t = torch.where(h_o_t == 1, random_t, t)
        neg_triplets = torch.stack((neg_h, r, neg_t), dim=1)
        all_triplets = torch.cat((triplets, neg_triplets), dim=0)
        labels = torch.zeros(all_triplets.size()[0])
        labels[:triplets.shape[0]] = 1
        return (all_triplets, labels)