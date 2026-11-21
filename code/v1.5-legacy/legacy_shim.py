"""legacy_shim.py -- O32 version-1.5 legacy code, compatibility layer (added in version 2.0).

The version-1.5 scripts hcolor_exact_check.py and verify_uomega.py imported
bfs_shells_depth_capped and compute_block_capacity_freq from a "unified"
spectral_O12.py that was never shipped. This module supplies both so that the
scripts run from this directory:

  bfs_shells_depth_capped(gens, q, max_depth)  BFS shells of the Cayley graph from the
      identity, shells 0..max_depth (same shell order and element order as
      spectral_O12.bfs_shells, which caps by a node fraction instead of a depth);
  compute_block_capacity_freq                  re-exported from ../sigma_freq.py.

STATUS: historical analysis. See README.md in this directory.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spectral_O12 import heisenberg_mul  # noqa: E402
from sigma_freq import compute_block_capacity_freq  # noqa: E402,F401


def bfs_shells_depth_capped(gens, q, max_depth):
    identity = (0, 0, 0)
    visited = {identity}
    current = [identity]
    shells = [current]
    for _ in range(max_depth):
        nxt = []
        for u in current:
            for g in gens:
                v = heisenberg_mul(u, g, q)
                if v not in visited:
                    visited.add(v)
                    nxt.append(v)
        if not nxt:
            break
        shells.append(nxt)
        current = nxt
    return shells
