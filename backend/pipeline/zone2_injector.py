from typing import Dict

def inject_zone2(reachable: Dict[str, int], levels_map: Dict[str, dict]) -> None:
    """
    Inject all nodes WHERE zone = 2 (GLOBAL).
    These bypass BFS but still need filtering.
    Mutates the reachable dictionary in-place.
    """
    zone2_ids = [k for k, v in levels_map.items() if v.get("zone") == 2]
    for z in zone2_ids:
        if z not in reachable:
            # Distance 99 for global constraints that are injected
            reachable[z] = 99
