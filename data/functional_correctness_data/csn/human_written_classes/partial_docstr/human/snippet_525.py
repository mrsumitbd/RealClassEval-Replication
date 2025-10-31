from anndata import AnnData
import numpy as np
from dataclasses import asdict, dataclass, field, fields

@dataclass
class EMParams:
    """EM parameters."""
    r2: np.ndarray = field(metadata={'is_matrix': False})
    alpha: np.ndarray = field(metadata={'is_matrix': False})
    beta: np.ndarray = field(metadata={'is_matrix': False})
    gamma: np.ndarray = field(metadata={'is_matrix': False})
    t_: np.ndarray = field(metadata={'is_matrix': False})
    scaling: np.ndarray = field(metadata={'is_matrix': False})
    std_u: np.ndarray = field(metadata={'is_matrix': False})
    std_s: np.ndarray = field(metadata={'is_matrix': False})
    likelihood: np.ndarray = field(metadata={'is_matrix': False})
    u0: np.ndarray = field(metadata={'is_matrix': False})
    s0: np.ndarray = field(metadata={'is_matrix': False})
    pval_steady: np.ndarray = field(metadata={'is_matrix': False})
    steady_u: np.ndarray = field(metadata={'is_matrix': False})
    steady_s: np.ndarray = field(metadata={'is_matrix': False})
    variance: np.ndarray = field(metadata={'is_matrix': False})
    alignment_scaling: np.ndarray = field(metadata={'is_matrix': False})
    T: np.ndarray = field(metadata={'is_matrix': True})
    Tau: np.ndarray = field(metadata={'is_matrix': True})
    Tau_: np.ndarray = field(metadata={'is_matrix': True})

    @classmethod
    def from_adata(cls, adata: AnnData, key: str='fit'):
        parameter_dict = {}
        for parameter in fields(cls):
            para_name = parameter.name
            if parameter.metadata['is_matrix']:
                if f'{key}_{para_name.lower()}' in adata.layers.keys():
                    parameter_dict[para_name] = adata.layers[f'{key}_{para_name.lower()}']
                else:
                    _vals = np.empty(adata.shape)
                    _vals.fill(np.nan)
                    parameter_dict[para_name] = _vals
            elif f'{key}_{para_name.lower()}' in adata.var.keys():
                parameter_dict[para_name] = adata.var[f'{key}_{para_name.lower()}'].values
            else:
                _vals = np.empty(adata.n_vars)
                _vals.fill(np.nan)
                parameter_dict[para_name] = _vals
        return cls(**parameter_dict)

    def export_to_adata(self, adata: AnnData, key: str='fit'):
        for parameter in fields(self):
            para_name = parameter.name
            value = getattr(self, para_name)
            if not np.all(np.isnan(value)):
                if parameter.metadata['is_matrix']:
                    adata.layers[f'{key}_{para_name.lower()}'] = value
                else:
                    adata.var[f'{key}_{para_name.lower()}'] = value
        return adata