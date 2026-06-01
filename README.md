# BRAHMO Rules Engine

**Zero-LLM Knowledge Graph Filtering Pipeline**

This repository contains the completed Developer Assessment 1 for the BRAHMO Rules Engine. It successfully implements an O(1) permission compiler and a deterministic BFS traversal pipeline that filters 842+ knowledge nodes down to a user-specific candidate set in under 500ms — with zero LLM involvement.

## 🚀 Key Features

*   **O(1) Permission Compilation:** Compiles a user's role and hierarchy ceiling into a hashmap once per session to eliminate the N+1 query problem during filtering.
*   **BFS DAG Traversal:** Starts at the user's department leaf node and traverses strictly upwards through the directed acyclic graph. Properly handles multi-parent nodes using a visited set to prevent infinite loops and duplicate processing.
*   **Zone 2 Injection:** Injects global hospital-wide safety constraints into the pipeline, regardless of the user's specific traversal path.
*   **GAP 5 Compliant:** Applies the "Permission Filter" (Check 3) *before* data is fetched from the database, ensuring unauthorized nodes never travel over the network.
*   **5-Check Sequential Filter:** 
    1.  **Isolation Check:** Multi-tenant organization boundaries.
    2.  **Compliance Check:** Array overlap checks to ensure `MNPI` and `CONFIDENTIAL` tags are strictly blocked from unauthorized users.
    3.  **Permission Check:** Hierarchy ceiling checks.
    4.  **Temporal Check:** Safely removes `SUPERSEDED` and expired nodes using ISO timestamps.
    5.  **Derivability Check:** Excludes high-derivability facts (like "Paracetamol is an analgesic") to save tokens downstream.
*   **Silent Exclusion:** No "access denied" errors. Unauthorized nodes are simply invisible.

## 💻 Tech Stack
- **Backend:** Python, FastAPI, Pydantic
- **Frontend:** Next.js, React, Tailwind CSS, Recharts
- **Database:** Supabase (PostgreSQL)

## 🛠️ How to Run Locally

### 1. Setup Environment
Ensure you have Python 3.11+ and Node.js v18+ installed.

### 2. Configure Database
Add your Supabase credentials to `.env` in the root folder:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### 3. Start the Backend
Open a terminal in the `backend` folder:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn supabase python-dotenv
python -m uvicorn main:app --reload --port 8000
```

### 4. Start the Frontend
Open a new terminal in the `frontend` folder:
```powershell
npm install
npm run dev
```
Navigate to `http://localhost:3000` to view the dashboard!

## 🧪 Demo Scenarios

The web interface provides 4 built-in scenarios that prove the pipeline's correctness:
1.  **The Core Pipeline:** Select Nurse Priya to see how the graph of 50 nodes filters down to exactly 15 nodes using the 5 sequential checks.
2.  **Same Graph, Different User:** Click "Run Scenario Comparison" to compare Nurse Priya, Dr. Vikram, and Admin Suresh. You will see that Dr. Vikram (HOD) receives 21 nodes while Suresh (Admin) receives over 30 nodes from the exact same graph query.
3.  **Silent Exclusion:** Note how Priya's pipeline contains 0 Cardiology nodes without throwing a single permission error.
4.  **Zone 2 Saves Lives:** Notice how globally critical constraints (e.g. Warfarin + NSAID interaction) are successfully injected into Priya's orthopedic session.

## 🏗️ Architecture
Read `docs/architecture.md` for an in-depth breakdown of the engineering decisions made to solve cycle prevention, multi-parent nodes, and GAP 5 database retrieval.
