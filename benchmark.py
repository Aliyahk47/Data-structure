"""Benchmarking utilities and plotting for VRP coursework.

Provides `plot_comparison(instances_info, outpath=...)` which mirrors the
plotting used in `vrp_coursework.py` but allows specifying an output path.
"""
from typing import List, Tuple
import matplotlib.pyplot as plt


def plot_comparison(instances_info: List[Tuple[str, object, dict]], outpath: str = 'vrp_comparison.png'):
    labels = []
    greedy_vals = []
    cw_vals = []
    for name, inst, res in instances_info:
        labels.append(name)
        greedy_vals.append(res['greedy'][0])
        cw_vals.append(res['clarke_wright'][0])

    x = range(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    ax.bar([i - width / 2 for i in x], greedy_vals, width, label='Greedy')
    ax.bar([i + width / 2 for i in x], cw_vals, width, label='Clarke-Wright + 2-opt')
    ax.set_ylabel('Total distance')
    ax.set_title('Algorithm comparison')
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


def plot_comparison(instances_info: List[Tuple[str, VRP, dict]], outpath: str = 'outputs/vrp_comparison.png') -> None:
    labels = []
    greedy_vals = []
    cw_vals = []
    for name, inst, res in instances_info:
        labels.append(name)
        greedy_vals.append(res['greedy'][0])
        cw_vals.append(res['clarke_wright'][0])

    x = range(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    ax.bar([i - width / 2 for i in x], greedy_vals, width, label='Greedy')
    ax.bar([i + width / 2 for i in x], cw_vals, width, label='Clarke-Wright + 2-opt')
    ax.set_ylabel('Total distance')
    ax.set_title('Algorithm comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)


if __name__ == '__main__':
    instances = []
    for n in (10, 20, 40):
        inst = generate_random_instance(n_customers=n, area_size=50, max_demand=4, vehicle_capacity=15, num_vehicles=6, seed=42 + n)
        res = benchmark(inst)
        instances.append((f'n={n}', inst, res))
        print(f"n={n}: greedy {res['greedy'][0]:.2f} vs cw {res['clarke_wright'][0]:.2f}")
    plot_comparison(instances)
    print('Saved outputs/vrp_comparison.png')
