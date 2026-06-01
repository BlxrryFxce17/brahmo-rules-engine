import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.bfs_traversal import traverse_bfs

def test_bfs_basic_traversal():
    levels_map = {
        "HL-10": {"id": "HL-10", "parent_ids": ["HL-08"], "zone": 1, "level_number": 10},
        "HL-08": {"id": "HL-08", "parent_ids": ["HL-05"], "zone": 1, "level_number": 8},
        "HL-05": {"id": "HL-05", "parent_ids": ["HL-01"], "zone": 1, "level_number": 5},
        "HL-01": {"id": "HL-01", "parent_ids": [], "zone": 1, "level_number": 1}
    }
    
    reachable = traverse_bfs("HL-10", levels_map)
    assert "HL-10" in reachable
    assert "HL-08" in reachable
    assert "HL-05" in reachable
    assert "HL-01" in reachable
    assert reachable["HL-10"] == 0
    assert reachable["HL-01"] == 3

def test_bfs_multi_parent_and_cycle_prevention():
    levels_map = {
        "HL-10": {"id": "HL-10", "parent_ids": ["HL-08A", "HL-08B"], "zone": 1, "level_number": 10},
        "HL-08A": {"id": "HL-08A", "parent_ids": ["HL-05"], "zone": 1, "level_number": 8},
        "HL-08B": {"id": "HL-08B", "parent_ids": ["HL-05"], "zone": 1, "level_number": 8},
        "HL-05": {"id": "HL-05", "parent_ids": ["HL-10"], "zone": 1, "level_number": 5}, # Cycle introduced
    }
    
    reachable = traverse_bfs("HL-10", levels_map)
    
    assert "HL-05" in reachable
    assert reachable["HL-10"] == 0
    assert reachable["HL-08A"] == 1
    assert reachable["HL-08B"] == 1
    assert reachable["HL-05"] == 2
    # Ensure cycle doesn't infinite loop and correctly visited set works
    assert len(reachable) == 4
