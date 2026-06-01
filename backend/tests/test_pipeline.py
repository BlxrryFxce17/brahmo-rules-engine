import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User
from pipeline.main_pipeline import run_pipeline

class MockResponse:
    def __init__(self, data):
        self.data = data

class MockQuery:
    def __init__(self, data):
        self.data = data
    def select(self, *args): return self
    def eq(self, *args): return self
    def in_(self, *args): return self
    def neq(self, *args): return self
    def lt(self, *args): return self
    def order(self, *args, **kwargs): return self
    def execute(self): return MockResponse(self.data)

class MockTable:
    def __init__(self, data):
        self.data = data
    def select(self, *args):
        return MockQuery(self.data)

class MockDB:
    def __init__(self, table_data):
        self.table_data = table_data
    def table(self, name):
        return MockTable(self.table_data.get(name, []))

def test_pipeline_integration():
    user = User(
        id="U-PRIYA",
        org_id="supra",
        name="Nurse Priya",
        role="VIEWER",
        department="ortho",
        ceiling_level=10,
        write_ceiling=None,
        compliance_clearance=[]
    )
    
    hierarchy_data = [
        {"id": "HL-10-ORTHO-W", "parent_ids": ["HL-08"], "zone": 1, "level_number": 10, "department": "ortho"},
        {"id": "HL-08", "parent_ids": [], "zone": 1, "level_number": 8, "department": "ortho"},
        {"id": "HL-GLOBAL", "parent_ids": [], "zone": 2, "level_number": 3, "department": None}
    ]
    
    nodes_data = [
        {"id": "N-1", "org_id": "supra", "type": "FACT", "content": "Test 1", "importance": 0.5, "zone": 1, "hierarchy_level_id": "HL-10-ORTHO-W", "derivability_score": 0.2},
        {"id": "N-GLOBAL", "org_id": "supra", "type": "CONSTRAINT", "content": "Global 1", "importance": 0.9, "zone": 2, "hierarchy_level_id": "HL-GLOBAL", "derivability_score": 0.2}
    ]
    
    db = MockDB({
        "hierarchy_levels": hierarchy_data,
        "knowledge_nodes": nodes_data
    })
    
    result = run_pipeline(user, db)
    
    assert result["user"] == "U-PRIYA"
    assert result["entry_point"] == "HL-10-ORTHO-W"
    
    # 2 nodes returned: N-1 (distance 0) and N-GLOBAL (distance 99, zone 2)
    assert len(result["candidate_nodes"]) == 2
    
    # Verify zone 2 injection and annotation
    ids = [n["id"] for n in result["candidate_nodes"]]
    assert "N-GLOBAL" in ids
