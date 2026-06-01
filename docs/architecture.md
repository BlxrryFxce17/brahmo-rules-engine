# BRAHMO Rules Engine Architecture

This document outlines the architectural decisions and pipeline logic for the BRAHMO Rules Engine, specifically designed for the Zero-LLM (L2) layer.

## Pipeline Design
The pipeline filters a graph of 842+ knowledge nodes down to a small, relevant candidate set for a specific user without using an LLM.

### 1. Permission Compilation (O(1) approach)
Instead of querying the database for every node to see if a user can access it (N+1 problem), permissions are compiled ONCE per session.
We map the user's role and hierarchy ceiling to a dictionary `{level: {can_read: bool, can_write: bool}}`. During the check phase, verifying access takes O(1) time.

### 2. BFS Traversal & Multi-Parent Handling
The knowledge graph is a Directed Acyclic Graph (DAG). We traverse upward starting from the user's department leaf node. 
A `visited` set is used during the Breadth-First Search. This:
- Prevents infinite loops in case of accidental cycles.
- Ensures nodes with multiple parents (e.g., a "Post-TKR Protocol" that belongs to both Orthopaedics and Surgery) are only processed once.

### 3. Zone 2 (Global) Injection
Global rules, such as hospital-wide safety constraints (e.g., "Never combine Warfarin with NSAIDs"), exist outside the standard department branches. We inject these nodes into the reachable set. They still undergo the 5 sequential checks to ensure they are current, non-derivable, and appropriate for the user's clearance.

### 4. The Five Checks & GAP 5
Checks are sequential. 
1. **Isolation** (org_id check)
2. **Compliance** (MNPI tags vs user clearance)
3. **Permission** (Hierarchy level vs user ceiling)
4. **Temporal** (Status and expiry)
5. **Derivability** (Excludes nodes the AI already knows)

**Addressing GAP 5:** 
Fetching all 842 nodes into Python memory and filtering them violates GAP 5 (restricted data retrieved before permission checks). To solve this, Checks 1 (Isolation), 3 (Permission pre-filter), 4 (Temporal), and 5 (Derivability) are pushed to the Supabase database via SQL query filters. Only nodes that pass these filters are returned over the network. 
*Note: Check 2 (Compliance array matching) is currently in application memory for demo purposes but can be pushed to a Supabase RPC in production.*

### 5. Derivability Scoring (Zero-LLM)
Derivability excludes facts the LLM inherently knows. Since L2 strictly prohibits LLM usage for filtering, derivability is a pre-computed score (0.0 to 1.0) stored on the node. A background batch job uses embeddings or keyword density to score nodes upon ingestion. The pipeline simply does a fast numeric comparison (`score < 0.7`).

## Security Model: Silent Exclusion
If a nurse attempts to query for Cardiology data, the API does not return a "403 Access Denied". Instead, it silently omits Cardiology nodes from the output. The response format remains identical, ensuring an attacker cannot infer the existence of hidden nodes.
