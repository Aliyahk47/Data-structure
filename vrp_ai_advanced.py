"""Advanced VRP solver: Clarke-Wright + 2-opt + Or-opt inter-route relocation."""
from typing import List, Tuple
from vrp_core import VRP
from vrp_improved import clarke_wright_savings, two_opt


def or_opt(vrp: VRP, routes: List[List[int]], segment_sizes: Tuple[int, ...] = (1, 2, 3)) -> List[List[int]]:
    """
    Or-opt inter-route relocation.

    For each route, tries to move a segment of length in `segment_sizes`
    from its current route and insert it at the best position in any
    other route. Accepts the move if it reduces total distance and
    the receiving route stays within capacity.

    Args:
        vrp:           VRP instance
        routes:        list of routes (each a list of customer indices)
        segment_sizes: segment lengths to try (default: 1, 2, 3 customers)
    Returns:
        Improved list of routes
    """
    routes = [r[:] for r in routes if r]
    improved = True

    while improved:
        improved = False

        for src_idx in range(len(routes)):
            if not routes[src_idx]:
                continue

            for seg_len in segment_sizes:
                if len(routes[src_idx]) < seg_len + 1:
                    continue

                for seg_start in range(len(routes[src_idx]) - seg_len + 1):
                    segment = routes[src_idx][seg_start: seg_start + seg_len]
                    seg_demand = sum(vrp.demands[c] for c in segment)

                    src_route = routes[src_idx]
                    before = src_route[seg_start - 1] if seg_start > 0 else None
                    after  = src_route[seg_start + seg_len] if seg_start + seg_len < len(src_route) else None

                    removal_gain = _removal_gain(vrp, before, segment, after)

                    best_gain = 1e-9
                    best_dst  = None
                    best_pos  = None

                    for dst_idx in range(len(routes)):
                        if dst_idx == src_idx:
                            continue

                        dst_load = sum(vrp.demands[c] for c in routes[dst_idx])
                        if dst_load + seg_demand > vrp.vehicle_capacity:
                            continue

                        dst_route = routes[dst_idx]
                        for pos in range(len(dst_route) + 1):
                            gain = _insertion_gain(vrp, dst_route, pos, segment)
                            total_gain = removal_gain + gain
                            if total_gain > best_gain:
                                best_gain = total_gain
                                best_dst  = dst_idx
                                best_pos  = pos

                    if best_dst is not None:
                        routes[src_idx] = (src_route[:seg_start] + src_route[seg_start + seg_len:])
                        routes[best_dst] = (routes[best_dst][:best_pos] + segment + routes[best_dst][best_pos:])
                        improved = True
                        break

                if improved:
                    break
            if improved:
                break

    routes = [r for r in routes if r]
    routes = [two_opt(vrp, r) for r in routes]
    return routes


def _node_dist(vrp: VRP, a, b) -> float:
    """Distance between two nodes where None means the depot (index 0)."""
    ai = 0 if a is None else a + 1
    bi = 0 if b is None else b + 1
    return vrp.distance_matrix[ai][bi]


def _removal_gain(vrp: VRP, before, segment: List[int], after) -> float:
    """Cost saved by removing segment from between before and after."""
    old = _node_dist(vrp, before, segment[0]) + _node_dist(vrp, segment[-1], after)
    new = _node_dist(vrp, before, after)
    return old - new


def _insertion_gain(vrp: VRP, route: List[int], pos: int, segment: List[int]) -> float:
    """Cost saved by inserting segment at position pos in route."""
    prev = route[pos - 1] if pos > 0          else None
    nxt  = route[pos]     if pos < len(route)  else None
    old  = _node_dist(vrp, prev, nxt)
    new  = _node_dist(vrp, prev, segment[0]) + _node_dist(vrp, segment[-1], nxt)
    return old - new


def solve(vrp: VRP) -> List[List[int]]:
    """Full pipeline: Clarke-Wright -> 2-opt -> Or-opt."""
    routes = clarke_wright_savings(vrp, do_2opt=True)
    return or_opt(vrp, routes)


__all__ = ["or_opt", "solve"]