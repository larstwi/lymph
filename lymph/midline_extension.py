import numpy as np
import pandas as pd
from typing import Union, Optional, List, Dict, Any

from pandas.core import base

from .unilateral import System
from .bilateral import BilateralSystem


class MidexSystem(BilateralSystem):
    """Model a bilateral lymphatic system where an additional risk factor can 
    be provided in the data: Whether or not the primary tumor extended over the 
    mid-sagittal line. 
    
    It is reasonable to assume (and supported by data) that such an extension 
    significantly increases the risk for metastatic spread to the contralateral 
    side of the neck. This subclass attempts to capture this using a simple 
    assumption: We assume that the probability of spread to the contralateral 
    side for patients *with* midline extension is larger than for patients 
    *without* it, but smaller than the probability of spread to the ipsilateral 
    side. Formally:
    
    .. math::
        b_c^{\\in} = \\alpha \cdot b_i + (1 - \\alpha) \cdot b_c^{\\not\\in}
        
    where :math:`b_c^{\\in}` is the probability of spread from the primary tumor 
    to the contralateral side for patients with midline extension, and 
    :math:`b_c^{\\not\\in}` for patients without. :math:`\\alpha` is the linear 
    mixing parameter.
    """
    
    def __init__(
        self, 
        graph: dict = {},
        alpha_mix: float = 0.,
        trans_symmetric: bool = True
    ):
        """"""
        super().__init__(
            graph=graph, 
            base_symmetric=False, 
            trans_symmetric=trans_symmetric
        )
        
        self.system["contra_ext"] = System(graph=graph)
        self.alpha_mix = alpha_mix
    
    
    @property
    def spread_probs(self) -> np.ndarray:
        """"""
        return np.concatenate([super().spread_probs, self.alpha_mix])
    
    @spread_probs.setter
    def spread_probs(self, new_spread_probs: np.ndarray):
        """"""
        self.alpha_mix = new_spread_probs[-1]
        
        # normal bilateral spread probs
        new_spread_probs = new_spread_probs[:-1]
        super().spread_probs.fset(self, new_spread_probs)
        
        # spread probs for contralateral side with midline extension
        len_base = len(self.system["ipsi"].base_edges)
        base_ipsi = self.system["ipsi"].spread_probs[:len_base]
        trans_ipsi = self.system["ipsi"].spread_probs[len_base:]
        base_contra = self.system["contra"].spread_probs[:len_base]
        
        base_ext = self.alpha_mix * base_ipsi + (1 - self.alpha_mix) * base_contra
        self.system["contra_ext"].spread_probs = np.concatenate(
            [base_ext, trans_ipsi]
        )
        