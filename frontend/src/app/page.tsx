"use client";

import { useState, useEffect } from "react";
import UserSelector from "../components/UserSelector";
import FilterFunnel from "../components/FilterFunnel";
import CandidateTable from "../components/CandidateTable";
import DAGViewer from "../components/DAGViewer";
import ComparisonView from "../components/ComparisonView";

export default function Home() {
  const [users, setUsers] = useState<any[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/users")
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        if (data && data.length > 0) {
          setSelectedUserId(data[0].id);
        }
      });
  }, []);

  const runPipeline = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/pipeline", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: selectedUserId }),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
      alert("Pipeline failed to run. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-neutral-950 text-white p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        <header className="border-b border-neutral-800 pb-6 flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-500">
              BRAHMO Rules Engine
            </h1>
            <p className="text-neutral-400 mt-2">BFS + 5-Check Filter Pipeline</p>
          </div>
          <div className="flex gap-4 items-end">
            <UserSelector users={users} value={selectedUserId} onChange={setSelectedUserId} />
            <button 
              onClick={runPipeline}
              disabled={loading || !selectedUserId}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 px-6 py-2 rounded-md font-medium transition-colors"
            >
              {loading ? "Running..." : "Run Pipeline"}
            </button>
          </div>
        </header>

        {result && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1 space-y-6">
               <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6">
                 <h2 className="text-lg font-semibold mb-4 text-neutral-200">Execution Timing</h2>
                 <ul className="space-y-2 text-sm text-neutral-400">
                   <li className="flex justify-between"><span>Permission Compile</span> <span>{result.pipeline_timing.permission_compile_ms.toFixed(2)} ms</span></li>
                   <li className="flex justify-between"><span>BFS Traversal</span> <span>{result.pipeline_timing.bfs_ms.toFixed(2)} ms</span></li>
                   <li className="flex justify-between"><span>Zone 2 Injection</span> <span>{result.pipeline_timing.zone2_inject_ms.toFixed(2)} ms</span></li>
                   <li className="flex justify-between"><span>Check 1 (Isolation)</span> <span>{result.pipeline_timing.check1_isolation_ms.toFixed(2)} ms</span></li>
                   <li className="flex justify-between"><span>Check 2 (Compliance)</span> <span>{result.pipeline_timing.check2_compliance_ms.toFixed(2)} ms</span></li>
                   <li className="flex justify-between"><span>Check 3 (Permission)</span> <span>{result.pipeline_timing.check3_permission_ms.toFixed(2)} ms</span></li>
                   <li className="flex justify-between"><span>Check 4 (Temporal)</span> <span>{result.pipeline_timing.check4_temporal_ms.toFixed(2)} ms</span></li>
                   <li className="flex justify-between"><span>Check 5 (Derivability)</span> <span>{result.pipeline_timing.check5_derivability_ms.toFixed(2)} ms</span></li>
                   <li className="flex justify-between font-bold text-white pt-2 border-t border-neutral-800">
                      <span>Total Time</span> <span>{result.pipeline_timing.total_ms.toFixed(2)} ms</span>
                   </li>
                 </ul>
               </div>

               <FilterFunnel stats={result.funnel} finalCount={result.candidate_nodes.length} />
               <DAGViewer result={result} />
            </div>

            <div className="lg:col-span-2 space-y-6">
               <ComparisonView />
               <CandidateTable nodes={result.candidate_nodes} />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
