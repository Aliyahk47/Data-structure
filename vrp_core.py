"""Small wrapper exposing core VRP helpers from vrp_coursework.

This module is a thin adapter so scripts (like tests.py) can import
`generate_random_instance` and `VRP` from a concise module name.
"""
from vrp_coursework import VRP, generate_random_instance, benchmark, plot_comparison

__all__ = ["VRP", "generate_random_instance", "benchmark", "plot_comparison"]
"""Core VRP data structures and helpers.

Contains the `VRP` class (distance matrix, distance utilities) and instance generator.
"""
import math
import random
from typing import List, Tuple

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
        matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    dx = points[i][0] - points[j][0]
                    dy = points[i][1] - points[j][1]
                    matrix[i][j] = math.hypot(dx, dy)
        return matrix

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


def generate_random_instance(n_customers: int, area_size: int = 100, max_demand: int = 5, vehicle_capacity: int = 15, num_vehicles: int = None, seed: int = None) -> VRP:
    if seed is not None:
        random.seed(seed)
    depot = (area_size / 2.0, area_size / 2.0)
    customers = [(random.uniform(0, area_size), random.uniform(0, area_size)) for _ in range(n_customers)]
    demands = [random.randint(1, max_demand) for _ in range(n_customers)]
    return VRP(depot, customers, demands, vehicle_capacity, num_vehicles=num_vehicles)
