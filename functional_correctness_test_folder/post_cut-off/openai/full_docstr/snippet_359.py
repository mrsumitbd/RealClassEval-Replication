
from typing import List, Tuple, Union, Iterable, Dict, Set
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors


class DRFPUtil:
    '''
    A utility class for encoding SMILES as drfp fingerprints.
    '''
    @staticmethod
