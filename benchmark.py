"""Benchmarking utilities and plotting for VRP coursework.

Provides `plot_comparison(instances_info, outpath=...)` which mirrors the
plotting used in `vrp_coursework.py` but allows specifying an output path.
"""
from typing import List, Tuple
import matplotlib.pyplot as plt


def plot_comparison(instances_info, outpath='outputs/final_comparison.png'):
    labels = []
    greedy_vals = []
    cw_vals = []
    or_vals = []  

    for name, inst, res in instances_info:
        labels.append(name)
        greedy_vals.append(res['greedy'][0])
        cw_vals.append(res['clarke_wright'][0])
        or_vals.append(res['or_opt'][0])  # Extract Or-opt results

    x = range(len(labels))
    width = 0.25 # Make bars thinner to fit three
    fig, ax = plt.subplots(figsize=(10, 6))

    # Add the three bar sets
    ax.bar([i - width for i in x], greedy_vals, width, label='Greedy')
    ax.bar([i for i in x], cw_vals, width, label='Clarke-Wright')
    ax.bar([i + width for i in x], or_vals, width, label='Or-opt + 2-opt')

    ax.set_ylabel('Total distance')
    ax.set_title('Algorithm Comparison (Including AI Or-opt)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    plt.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)

__all__ = ['plot_comparison']
"""Benchmarking utilities that compare naive and improved solvers and write graphs to outputs/.
"""
from typing import List, Tuple
import time
import matplotlib.pyplot as plt

from vrp_core import VRP, generate_random_instance
from vrp_naive import greedy_nearest_neighbor
from vrp_improved import clarke_wright_savings


def benchmark(instance: VRP) -> dict:
    results = {}
    t0 = time.time()
    g = greedy_nearest_neighbor(instance)
    tg = time.time() - t0
    dg = instance.total_distance(g)
    results['greedy'] = (dg, tg, g)

    t0 = time.time()
    cw = clarke_wright_savings(instance, do_2opt=True)
    tcw = time.time() - t0
    dcw = instance.total_distance(cw)
    results['clarke_wright'] = (dcw, tcw, cw)
    return results
