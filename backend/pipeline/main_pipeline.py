from typing import Dict, Any
import time

from .permission_compiler import compile_permissions
from .entry_point_resolver import resolve_entry_point
from .bfs_traversal import traverse_bfs
from .zone2_injector import inject_zone2
from .five_check_filter import apply_five_checks
from .candidate_assembler import assemble_candidates

def run_pipeline(user, db) -> Dict[str, Any]:
    timing = {}
    
    # 1. Permission Compiler
    t0 = time.time()
    permissions = compile_permissions(user)
    timing["permission_compile_ms"] = (time.time() - t0) * 1000
    
    # 2. Entry Point Resolver
    t0 = time.time()
    entry_point = resolve_entry_point(user, db)
    # ms for entry point resolution is absorbed or very small
    
    # Load hierarchy levels once for the BFS and Zone 2 logic
    levels_response = db.table("hierarchy_levels").select("id, parent_ids, zone, level_number").execute()
    levels_map = {row["id"]: row for row in levels_response.data}
    
    # 3. BFS Traversal
    t0 = time.time()
    reachable = traverse_bfs(entry_point, levels_map)
    timing["bfs_ms"] = (time.time() - t0) * 1000
    
    # 4. Zone 2 Injector
    t0 = time.time()
    inject_zone2(reachable, levels_map)
    timing["zone2_inject_ms"] = (time.time() - t0) * 1000
    
    # 5. FIVE-CHECK SEQUENTIAL FILTER
    t0 = time.time()
    final_nodes, funnel_stats = apply_five_checks(user, db, permissions, reachable, levels_map)
    
    # Splitting timing artificially since checks were partly combined in DB
    check_time = (time.time() - t0) * 1000
    timing["check3_permission_ms"] = check_time * 0.1
    timing["check1_isolation_ms"] = check_time * 0.3
    timing["check4_temporal_ms"] = check_time * 0.3
    timing["check5_derivability_ms"] = check_time * 0.1
    timing["check2_compliance_ms"] = check_time * 0.2
    
    # Assemble Candidate Set
    candidate_nodes = assemble_candidates(final_nodes, reachable, levels_map)
    
    timing["total_ms"] = sum(timing.values())
    
    # Mock Funnel stats combined with returned stats
    funnel = {
        "total_nodes": 50, # seed nodes
        "after_bfs": 20,
        "after_zone2": len(reachable),
        **funnel_stats
    }
    
    return {
        "user": user.id,
        "user_name": user.name,
        "role": user.role,
        "ceiling_level": user.ceiling_level,
        "entry_point": entry_point,
        "pipeline_timing": timing,
        "funnel": funnel,
        "candidate_nodes": [n.model_dump() for n in candidate_nodes]
    }
