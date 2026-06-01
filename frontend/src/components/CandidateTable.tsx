export default function CandidateTable({ nodes }: { nodes: any[] }) {
  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-lg overflow-hidden shadow-xl">
      <div className="px-6 py-4 border-b border-neutral-800 flex justify-between items-center">
        <h2 className="text-lg font-semibold text-neutral-200">Candidate Set ({nodes.length} nodes)</h2>
      </div>
      <div className="overflow-x-auto max-h-[800px] overflow-y-auto">
        <table className="w-full text-sm text-left text-neutral-400">
          <thead className="text-xs text-neutral-500 uppercase bg-neutral-950/50 sticky top-0 z-10">
            <tr>
              <th className="px-6 py-3">Type</th>
              <th className="px-6 py-3">Content</th>
              <th className="px-6 py-3">Dist</th>
              <th className="px-6 py-3">Zone</th>
              <th className="px-6 py-3">Hint</th>
            </tr>
          </thead>
          <tbody>
            {nodes.map((n, i) => (
              <tr key={n.id} className="border-b border-neutral-800 hover:bg-neutral-800/50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap align-top">
                  <span className={`px-2 py-1 rounded text-xs font-bold tracking-wider ${
                    n.type === 'CONSTRAINT' ? 'bg-red-900/30 text-red-400 border border-red-800/50' :
                    n.type === 'DECISION' ? 'bg-yellow-900/30 text-yellow-400 border border-yellow-800/50' :
                    n.type === 'ANTI_PATTERN' ? 'bg-orange-900/30 text-orange-400 border border-orange-800/50' :
                    'bg-blue-900/30 text-blue-400 border border-blue-800/50'
                  }`}>
                    {n.type}
                  </span>
                </td>
                <td className="px-6 py-4 text-neutral-300 align-top max-w-md">
                  <div className="font-medium text-white mb-1.5 flex items-center gap-2">
                     <span>{n.id}</span>
                     <span className="text-[10px] text-neutral-500 bg-neutral-800 px-1.5 py-0.5 rounded">Level {n.hierarchy_level}</span>
                  </div>
                  <div className="text-sm leading-relaxed opacity-90">{n.content}</div>
                </td>
                <td className="px-6 py-4 font-mono align-top text-center text-neutral-500">{n.distance_from_entry}</td>
                <td className="px-6 py-4 font-mono align-top text-center text-neutral-500">{n.zone}</td>
                <td className="px-6 py-4 align-top">
                  <span className="text-xs font-mono text-neutral-500">{n.compression_hint}</span>
                </td>
              </tr>
            ))}
            {nodes.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-neutral-500">
                  No nodes passed the filter for this user.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
