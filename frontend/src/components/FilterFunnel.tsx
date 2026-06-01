export default function FilterFunnel({ stats, finalCount }: { stats: any, finalCount: number }) {
  const max = stats.total_nodes;
  const stages = [
    { label: "Total Nodes", value: stats.total_nodes },
    { label: "After BFS Reach", value: stats.after_bfs },
    { label: "+ Zone 2 Global", value: stats.after_zone2 },
    { label: "1. Isolation Pass", value: stats.after_check1 },
    { label: "2. Compliance Pass", value: stats.after_check2 },
    { label: "3. Permission Pass", value: stats.after_check3 },
    { label: "4. Temporal Pass", value: stats.after_check4 },
    { label: "5. Derivability Pass", value: stats.after_check5 },
    { label: "Final Candidate Set", value: finalCount },
  ];

  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6">
      <h2 className="text-lg font-semibold mb-6 text-neutral-200">Filter Funnel</h2>
      <div className="space-y-4">
        {stages.map((s, i) => (
          <div key={i} className="relative">
            <div className="flex justify-between text-xs text-neutral-400 mb-1 z-10 relative">
              <span>{s.label}</span>
              <span className="font-mono">{s.value}</span>
            </div>
            <div className="w-full bg-neutral-800 rounded-full h-2">
              <div 
                className="bg-indigo-500 h-2 rounded-full transition-all duration-500" 
                style={{ width: `${(s.value / max) * 100}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
