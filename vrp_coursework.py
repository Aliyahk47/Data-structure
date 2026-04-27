"""vrp_coursework.py
A small coursework module for Vehicle Routing Problem (VRP).

Provides:
- data structures for depot/customers/demands
- naive greedy (nearest neighbour) solver
- Clarke-Wright savings solver with optional 2-opt local search
- Or-opt inter-route relocation solver
- benchmarking utilities and simple plotting

Run as a script to see an example and generate comparison plots.
"""
import math
import random
import time
from typing import List, Tuple

import matplotlib.pyplot as plt


Point = Tuple[float, float]


class VRP:
    def __init__(self, depot: Point, customers: List[Point], demands: List[int], vehicle_capacity: int, num_vehicles: int = None):
        self.depot = depot
        self.customers = customers
        self.demands = demands
        self.vehicle_capacity = vehicle_capacity
        self.num_vehicles = num_vehicles
        self.n = len(customers)
        self.distance_matrix = self._compute_distance_matrix()

    def _compute_distance_matrix(self) -> List[List[float]]:
        points = [self.depot] + self.customers
        n = len(points)
        m = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    dx = points[i][0] - points[j][0]
                    dy = points[i][1] - points[j][1]
                    m[i][j] = math.hypot(dx, dy)
        return m

    def total_distance(self, routes: List[List[int]]) -> float:
        total = 0.0
        for route in routes:
            if not route:
                continue
            prev = 0
            for c in route:
                total += self.distance_matrix[prev][c + 1]
                prev = c + 1
            total += self.distance_matrix[prev][0]
        return total

    def greedy_nearest_neighbor(self) -> List[List[int]]:
        unvisited = set(range(self.n))
        routes = []
        for _ in range(self.num_vehicles or self.n):
            if not unvisited:
                break
            route = []
            load = 0
            current = 0
            while True:
                candidates = [c for c in unvisited if load + self.demands[c] <= self.vehicle_capacity]
                if not candidates:
                    break
                nearest = min(candidates, key=lambda c: self.distance_matrix[current][c + 1])
                route.append(nearest)
                load += self.demands[nearest]
                unvisited.remove(nearest)
                current = nearest + 1
            routes.append(route)
        return routes

    def clarke_wright_savings(self, do_2opt: bool = True) -> List[List[int]]:
        routes = {i: [i] for i in range(self.n)}
        route_load = {i: self.demands[i] for i in range(self.n)}

        savings = []
        for i in range(self.n):
            for j in range(i + 1, self.n):
                sij = self.distance_matrix[0][i + 1] + self.distance_matrix[0][j + 1] - self.distance_matrix[i + 1][j + 1]
                savings.append((sij, i, j))
        savings.sort(reverse=True)

        def find_route(containing: int):
            for rid, r in routes.items():
                if containing in r:
                    return rid
            return None

        for s, i, j in savings:
            ri = find_route(i)
            rj = find_route(j)
            if ri is None or rj is None or ri == rj:
                continue
            r_i = routes[ri]
            r_j = routes[rj]
            if (i == r_i[0] or i == r_i[-1]) and (j == r_j[0] or j == r_j[-1]):
                combined_load = route_load[ri] + route_load[rj]
                if combined_load <= self.vehicle_capacity:
                    if i == r_i[-1] and j == r_j[0]:
                        new_route = r_i + r_j
                    elif i == r_i[0] and j == r_j[-1]:
                        new_route = list(reversed(r_i)) + list(reversed(r_j))
                    elif i == r_i[-1] and j == r_j[-1]:
                        new_route = r_i + list(reversed(r_j))
                    else:
                        new_route = list(reversed(r_i)) + r_j
                    new_id = min(ri, rj)
                    del routes[ri]
                    del routes[rj]
                    routes[new_id] = new_route
                    route_load[new_id] = combined_load

        result_routes = list(routes.values())

        if do_2opt:
            for idx, r in enumerate(result_routes):
                result_routes[idx] = self._two_opt_route(r)

        return result_routes

    def _two_opt_route(self, route: List[int], max_iter: int = 100) -> List[int]:
        if len(route) < 3:
            return route
        best = route[:]
        improved = True
        it = 0
        while improved and it < max_iter:
            improved = False
            it += 1
            for i in range(0, len(best) - 2):
                for j in range(i + 2, len(best)):
                    if j - i == 1:
                        continue
                    new_route = best[:i + 1] + list(reversed(best[i + 1:j + 1])) + best[j + 1:]
                    if self._route_distance(new_route) + 1e-9 < self._route_distance(best):
                        best = new_route
                        improved = True
                        break
                if improved:
                    break
        return best

    def _route_distance(self, route: List[int]) -> float:
        if not route:
            return 0.0
        d = 0.0
        prev = 0
        for c in route:
            d += self.distance_matrix[prev][c + 1]
            prev = c + 1
        d += self.distance_matrix[prev][0]
        return d


def generate_random_instance(n_customers: int, area_size: int = 100, max_demand: int = 5, vehicle_capacity: int = 15, num_vehicles: int = None, seed: int = None):
    if seed is not None:
        random.seed(seed)
    depot = (area_size / 2.0, area_size / 2.0)
    customers = [(random.uniform(0, area_size), random.uniform(0, area_size)) for _ in range(n_customers)]
    demands = [random.randint(1, max_demand) for _ in range(n_customers)]
    return VRP(depot, customers, demands, vehicle_capacity, num_vehicles=num_vehicles)


def benchmark(instance: VRP):
    # imported here instead of top of file to avoid circular import:
    # vrp_ai_advanced -> vrp_core -> vrp_coursework -> vrp_ai_advanced
    from vrp_ai_advanced import solve as or_opt_solve

    results = {}

    # --- Greedy nearest neighbour ---
    t0 = time.time()
    g_routes = instance.greedy_nearest_neighbor()
    tg = time.time() - t0
    results['greedy'] = (instance.total_distance(g_routes), tg, g_routes)

    # --- Clarke-Wright + 2-opt ---
    t0 = time.time()
    cw_routes = instance.clarke_wright_savings(do_2opt=True)
    tcw = time.time() - t0
    results['clarke_wright'] = (instance.total_distance(cw_routes), tcw, cw_routes)

    # --- Clarke-Wright + 2-opt + Or-opt ---
    t0 = time.time()
    or_routes = or_opt_solve(instance)
    tor = time.time() - t0
    results['or_opt'] = (instance.total_distance(or_routes), tor, or_routes)

    return results


def plot_comparison(instances_info: List[Tuple[str, VRP, dict]]):
    import os
    os.makedirs('outputs', exist_ok=True)

    labels      = []
    greedy_vals = []
    cw_vals     = []
    or_vals     = []

    for name, inst, res in instances_info:
        labels.append(name)
        greedy_vals.append(res['greedy'][0])
        cw_vals.append(res['clarke_wright'][0])
        or_vals.append(res['or_opt'][0])

    x     = list(range(len(labels)))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar([i - width for i in x], greedy_vals, width, label='Greedy NN',              color='C0')
    ax.bar([i          for i in x], cw_vals,    width, label='Clarke-Wright + 2-opt',  color='C1')
    ax.bar([i + width  for i in x], or_vals,    width, label='Clarke-Wright + Or-opt', color='C2')

    ax.set_ylabel('Total distance')
    ax.set_title('Algorithm comparison: Greedy vs Clarke-Wright vs Or-opt')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.tight_layout()
    plt.savefig('outputs/vrp_comparison.png')
    plt.close()
    print('Saved comparison plot to outputs/vrp_comparison.png')


if __name__ == '__main__':
    instances = []
    for n in (10, 20, 40):
        inst = generate_random_instance(
            n_customers=n, area_size=50, max_demand=4,
            vehicle_capacity=15, num_vehicles=6, seed=42 + n
        )
        res = benchmark(inst)
        instances.append((f'n={n}', inst, res))
        print(
            f"Instance n={n}: "
            f"greedy={res['greedy'][0]:.2f} ({res['greedy'][1]:.4f}s) | "
            f"clarke_wright={res['clarke_wright'][0]:.2f} ({res['clarke_wright'][1]:.4f}s) | "
            f"or_opt={res['or_opt'][0]:.2f} ({res['or_opt'][1]:.4f}s)"
        )

    plot_comparison(instances)