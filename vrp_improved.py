"""Improved solver wrapper: exposes Clarke-Wright savings solver.
"""
def clarke_wright_savings(instance):
    """Return routes produced by Clarke-Wright savings (with 2-opt).

    Args:
        instance: a VRP instance (from vrp_coursework.VRP)
    Returns:
        List of routes (list of customer indices)
    """
    return instance.clarke_wright_savings(do_2opt=False)

__all__ = ["clarke_wright_savings"]
"""Improved VRP solver: Clarke-Wright savings + optional 2-opt local search.
"""
from typing import List
from vrp_core import VRP


def clarke_wright_savings(vrp: VRP, do_2opt: bool = True) -> List[List[int]]:
    routes = {i: [i] for i in range(vrp.n)}
    route_load = {i: vrp.demands[i] for i in range(vrp.n)}

    savings = []
    for i in range(vrp.n):
        for j in range(i + 1, vrp.n):
            s = vrp.distance_matrix[0][i + 1] + vrp.distance_matrix[0][j + 1] - vrp.distance_matrix[i + 1][j + 1]
            savings.append((s, i, j))
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
            combined = route_load[ri] + route_load[rj]
            if combined <= vrp.vehicle_capacity:
                if i == r_i[-1] and j == r_j[0]:
                    new = r_i + r_j
                elif i == r_i[0] and j == r_j[-1]:
                    new = list(reversed(r_i)) + list(reversed(r_j))
                elif i == r_i[-1] and j == r_j[-1]:
                    new = r_i + list(reversed(r_j))
                else:
                    new = list(reversed(r_i)) + r_j
                new_id = min(ri, rj)
                del routes[ri]
                del routes[rj]
                routes[new_id] = new
                route_load[new_id] = combined

    result = list(routes.values())

    if do_2opt:
        for idx, r in enumerate(result):
            result[idx] = two_opt(vrp, r)

    return result


def two_opt(vrp: VRP, route: List[int], max_iter: int = 100) -> List[int]:
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
                cand = best[:i + 1] + list(reversed(best[i + 1:j + 1])) + best[j + 1:]
                if vrp._route_distance(cand) + 1e-9 < vrp._route_distance(best):
                    best = cand
                    improved = True
                    break
            if improved:
                break
    return best
