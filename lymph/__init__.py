"""This package contains code to model the spread of microscopic metastases
through a system of lymph node levels (LNLs), using either a Bayesian network
or a hidden Markov model."""

__description__ = "Package for statistical modelling of lymphatic metastatic spread."
__author__ = "Roman Ludwig"
__email__ = "roman.ludwig@usz.ch"
__uri__ = "https://github.com/rmnldwg/lymph"

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .node import node_trans_prob, Node
from .edge import Edge
from .unilateral import change_base, Unilateral, System
from .bilateral import Bilateral, BilateralSystem
from .midline import MidlineBilateral

__all__ = [
    "Node",
    "Edge",
    "Unilateral", "System",
    "Bilateral", "BilateralSystem",
    "MidlineBilateral"
    "change_base",
]