from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class CandidateNode(BaseModel):
    id: str
    type: str
    content: str
    importance: float
    zone: int
    hierarchy_level: int
    distance_from_entry: int
    compression_hint: str

class PipelineTiming(BaseModel):
    permission_compile_ms: float
    bfs_ms: float
    zone2_inject_ms: float
    check1_isolation_ms: float
    check2_compliance_ms: float
    check3_permission_ms: float
    check4_temporal_ms: float
    check5_derivability_ms: float
    total_ms: float

class FunnelStats(BaseModel):
    total_nodes: int
    after_bfs: int
    after_zone2: int
    after_check1: int
    after_check2: int
    after_check3: int
    after_check4: int
    after_check5: int

class CandidateSetResponse(BaseModel):
    user: str
    user_name: str
    role: str
    ceiling_level: int
    entry_point: str
    pipeline_timing: PipelineTiming
    funnel: FunnelStats
    candidate_nodes: List[CandidateNode]
