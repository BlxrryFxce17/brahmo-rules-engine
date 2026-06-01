import React, { useState } from 'react';

export default function ComparisonView() {
  const [comparing, setComparing] = useState(false);
  const [results, setResults] = useState<any>(null);

  const runComparison = async () => {
    setComparing(true);
    try {
      const u1 = await fetch("http://localhost:8000/pipeline", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ user_id: 'U-PRIYA' })
      }).then(r => r.json());
      const u2 = await fetch("http://localhost:8000/pipeline", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ user_id: 'U-VIKRAM' })
      }).then(r => r.json());
      const u3 = await fetch("http://localhost:8000/pipeline", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ user_id: 'U-SURESH' })
      }).then(r => r.json());
      setResults({ u1, u2, u3 });
    } catch (e) {
      console.error(e);
      alert("Failed to run comparison. Ensure backend is running.");
    } finally {
      setComparing(false);
    }
  };

  if (!results) {
    return (
      <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 flex justify-center items-center h-48">
        <button onClick={runComparison} disabled={comparing} className="bg-indigo-600 hover:bg-indigo-500 px-6 py-2 rounded-md font-medium transition-colors">
          {comparing ? "Running Scenarios..." : "Run Scenario Comparison"}
        </button>
      </div>
    );
  }

  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 overflow-x-auto">
      <h2 className="text-lg font-semibold mb-4 text-neutral-200">User Scenarios (Same Graph)</h2>
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-neutral-800 text-neutral-400">
            <th className="py-2">Metric</th>
            <th className="py-2">Nurse Priya (L10)</th>
            <th className="py-2">Dr. Vikram (L4)</th>
            <th className="py-2">Admin Suresh (L1)</th>
          </tr>
        </thead>
        <tbody className="text-neutral-300">
          <tr className="border-b border-neutral-800/50">
            <td className="py-3 font-medium text-white">BFS Reach</td>
            <td>~{results.u1.funnel.after_bfs} nodes</td>
            <td>~{results.u2.funnel.after_bfs} nodes</td>
            <td>~{results.u3.funnel.after_bfs} nodes</td>
          </tr>
          <tr className="border-b border-neutral-800/50">
            <td className="py-3 font-medium text-white">+ Zone 2 Injection</td>
            <td>~{results.u1.funnel.after_zone2} nodes</td>
            <td>~{results.u2.funnel.after_zone2} nodes</td>
            <td>~{results.u3.funnel.after_zone2} nodes</td>
          </tr>
          <tr className="border-b border-neutral-800/50 text-indigo-400 font-semibold text-base">
            <td className="py-3">Final Output Count</td>
            <td>{results.u1.candidate_nodes.length} nodes</td>
            <td>{results.u2.candidate_nodes.length} nodes</td>
            <td>{results.u3.candidate_nodes.length} nodes</td>
          </tr>
          <tr>
            <td className="py-3 text-neutral-400">Pipeline Time</td>
            <td className="text-neutral-400">{results.u1.pipeline_timing.total_ms.toFixed(1)} ms</td>
            <td className="text-neutral-400">{results.u2.pipeline_timing.total_ms.toFixed(1)} ms</td>
            <td className="text-neutral-400">{results.u3.pipeline_timing.total_ms.toFixed(1)} ms</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
