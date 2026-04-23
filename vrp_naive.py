"""Naive solver wrapper: exposes a simple greedy nearest-neighbour function.
"""
def greedy_nearest_neighbor(instance):
    """Return routes built by the instance's greedy method.

    Args:
        instance: a VRP instance (from vrp_coursework.VRP)
    Returns:
        List of routes (list of customer indices)
    """
    return instance.greedy_nearest_neighbor()

__all__ = ["greedy_nearest_neighbor"]
"""Naive/initial VRP solver (greedy nearest-neighbour).
"""
from typing import List
from vrp_core import VRP


def greedy_nearest_neighbor(vrp: VRP) -> List[List[int]]:
    unvisited = set(range(vrp.n))
    routes = []
    for _ in range(vrp.num_vehicles or vrp.n):
        if not unvisited:
            break
        route = []
        load = 0
        current = 0
        while True:
            candidates = [c for c in unvisited if load + vrp.demands[c] <= vrp.vehicle_capacity]
            if not candidates:
                break
            nearest = min(candidates, key=lambda c: vrp.distance_matrix[current][c + 1])
            route.append(nearest)
            load += vrp.demands[nearest]
            unvisited.remove(nearest)
            current = nearest + 1
        routes.append(route)
    return routes
