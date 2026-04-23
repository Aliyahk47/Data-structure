"""Simple tests harness: up to 5 tests. Each test runs both solvers and saves a small result plot.
"""
from vrp_core import generate_random_instance
from vrp_naive import greedy_nearest_neighbor
from vrp_improved import clarke_wright_savings
from benchmark import plot_comparison
import matplotlib.pyplot as plt
import os


TESTS = [
    {'name': 'tiny', 'n': 5, 'seed': 1},
    {'name': 'small', 'n': 10, 'seed': 2},
    {'name': 'medium', 'n': 20, 'seed': 3},
]


def run_tests(tests=TESTS):
    os.makedirs('outputs', exist_ok=True)
    instances_info = []
    for t in tests[:5]:
        inst = generate_random_instance(n_customers=t['n'], area_size=50, max_demand=4, vehicle_capacity=15, num_vehicles=6, seed=t.get('seed'))
        g = greedy_nearest_neighbor(inst)
        cw = clarke_wright_savings(inst)
        dg = inst.total_distance(g)
        dcw = inst.total_distance(cw)
        print(f"Test {t['name']}: greedy={dg:.2f}, cw={dcw:.2f}")
        instances_info.append((t['name'], inst, {'greedy': (dg, None, g), 'clarke_wright': (dcw, None, cw)}))
        # per-test small bar
        fig, ax = plt.subplots()
        ax.bar(['greedy', 'cw'], [dg, dcw], color=['C0', 'C1'])
        ax.set_title(f"{t['name']} distances")
        fig.savefig(f"outputs/test_{t['name']}.png")
        plt.close(fig)
    # summary comparison
    plot_comparison(instances_info, outpath='outputs/summary_comparison.png')
    print('Saved per-test plots to outputs/')


if __name__ == '__main__':
    run_tests()
