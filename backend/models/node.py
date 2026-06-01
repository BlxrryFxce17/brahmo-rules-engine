from pydantic import BaseModel
from typing import List, Optional

class Node(BaseModel):
    id: str
    org_id: str
    hierarchy_level_id: str
    type: str
    title: str
    content: str
    importance: float
    zone: int
    status: str
    derivability_score: float
    compliance_tags: List[str] = []
    valid_until: Optional[str] = None
    superseded_by: Optional[str] = None
    department: Optional[str] = None
