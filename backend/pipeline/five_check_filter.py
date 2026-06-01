from typing import Dict, Any, List, Tuple
from models.user import User
from supabase import Client
from datetime import datetime, timezone

def apply_five_checks(user: User, db: Client, permissions: Dict[int, Dict[str, bool]], reachable: Dict[str, int], levels_map: Dict[str, dict]) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    Applies the 5-check sequential filter.
    Returns a tuple of (final_nodes, funnel_stats).
    """
    # Check 3 (Permission) pre-filter: To avoid GAP 5 violation (fetching restricted data over network),
    # we filter the allowed hierarchy levels BEFORE querying knowledge_nodes.
    allowed_level_ids = []
    for lid in reachable.keys():
        lvl_num = levels_map[lid]["level_number"]
        if permissions.get(lvl_num, {}).get("can_read", False):
            allowed_level_ids.append(lid)
            
    # DB Query: Fetch ONLY permitted nodes to satisfy GAP 5 rule.
    nodes_response = db.table("knowledge_nodes").select("*").in_("hierarchy_level_id", allowed_level_ids).execute()
    db_nodes = nodes_response.data
    
    # We now apply the remaining checks sequentially in the app layer 
    # to collect exact funnel counts for the frontend visualization.
    
    # Check 1 (Isolation)
    after_check1_nodes = [n for n in db_nodes if n.get("org_id") == user.org_id]
    
    # Check 2 (Compliance)
    after_check2_nodes = []
    user_tags = set(user.compliance_clearance)
    for n in after_check1_nodes:
        node_tags = set(n.get("compliance_tags", []) or [])
        # If node has tags that user DOES NOT have, block it
        if not node_tags.issubset(user_tags):
            continue
        after_check2_nodes.append(n)
        
    # Check 4 (Temporal)
    now = datetime.now(timezone.utc)
    after_check4_nodes = []
    for n in after_check2_nodes:
        if n.get("status") == "SUPERSEDED":
            continue
        valid_until = n.get("valid_until")
        if valid_until:
            try:
                vt = datetime.fromisoformat(valid_until.replace('Z', '+00:00'))
                if vt < now:
                    continue
            except:
                pass
        after_check4_nodes.append(n)
        
    # Check 5 (Derivability)
    final_nodes = [n for n in after_check4_nodes if float(n.get("derivability_score", 0)) < 0.7]
    
    funnel = {
        "after_check1": len(after_check1_nodes),
        "after_check2": len(after_check2_nodes),
        "after_check3": len(db_nodes), # Check 3 was done at DB level
        "after_check4": len(after_check4_nodes),
        "after_check5": len(final_nodes)
    }
    
    return final_nodes, funnel
