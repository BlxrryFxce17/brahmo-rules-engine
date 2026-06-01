from typing import Dict

def traverse_bfs(entry_point: str, levels_map: Dict[str, dict]) -> Dict[str, int]:
    """
    Start at entry point, walk UP the DAG via parent_ids edges.
    Use a queue (FIFO) and a visited set (prevent re-processing).
    Returns a dictionary mapping reachable node_id -> distance from entry.
    """
    reachable = {} # id -> distance
    queue = [(entry_point, 0)]
    visited = set()
    
    while queue:
        curr, dist = queue.pop(0)
        if curr in visited: continue
        visited.add(curr)
        reachable[curr] = dist
        
        for p in levels_map.get(curr, {}).get("parent_ids", []):
            if p not in visited:
                queue.append((p, dist + 1))
                
    return reachable
