from typing import Dict, Any, List
from models.candidate_set import CandidateNode

def assemble_candidates(final_nodes: List[Dict[str, Any]], reachable: Dict[str, int], levels_map: Dict[str, dict]) -> List[CandidateNode]:
    """
    Take surviving nodes and annotate them.
    """
    candidate_nodes = []
    for node in final_nodes:
        dist = reachable.get(node["hierarchy_level_id"], 0)
        hint = "FULL" if dist <= 1 else ("COMPRESSED" if dist == 2 else "CONSTRAINT_ONLY")
        
        candidate_nodes.append(CandidateNode(
            id=node["id"],
            type=node["type"],
            content=node["content"],
            importance=node["importance"],
            zone=node["zone"],
            hierarchy_level=levels_map[node["hierarchy_level_id"]]["level_number"],
            distance_from_entry=dist,
            compression_hint=hint
        ))
        
    return candidate_nodes
