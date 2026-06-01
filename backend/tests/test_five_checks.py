import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User
from pipeline.five_check_filter import apply_five_checks

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

def test_five_checks():
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
    
    # permissions where levels >= 10 can be read
    permissions = {
        10: {"can_read": True, "can_write": False},
        8: {"can_read": False, "can_write": False}
    }
    
    reachable = {"HL-10": 0, "HL-08": 1}
    
    levels_map = {
        "HL-10": {"level_number": 10},
        "HL-08": {"level_number": 8}
    }
    
    # Mocking database to return nodes that passed checks 1, 4, 5
    nodes_data = [
        {"id": "N-O01", "compliance_tags": [], "org_id": "supra", "hierarchy_level_id": "HL-10"},
        {"id": "N-O02", "compliance_tags": ["MNPI"], "org_id": "supra", "hierarchy_level_id": "HL-10"} # blocked by compliance
    ]
    
    db = MockDB({"knowledge_nodes": nodes_data})
    
    final_nodes, funnel = apply_five_checks(user, db, permissions, reachable, levels_map)
    
    assert len(final_nodes) == 1
    assert final_nodes[0]["id"] == "N-O01"
    # Verify N-O02 was excluded because of MNPI tag (Compliance check)
