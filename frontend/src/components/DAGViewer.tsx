import React from 'react';

export default function DAGViewer({ result }: { result: any }) {
  if (!result) return null;
  
  const reachableLevels = new Set(result.candidate_nodes.map((n: any) => n.hierarchy_level));
  
  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6">
      <h2 className="text-lg font-semibold mb-4 text-neutral-200">DAG Visualization</h2>
      <div className="space-y-2 text-sm font-mono">
        <div className={reachableLevels.has(1) ? "text-green-400" : "text-neutral-600"}>
           [L1] Supra Hospital {result.entry_point === 'HL-01' ? '← ENTRY' : ''}
        </div>
        <div className="pl-4 border-l border-neutral-700 ml-2">
          <div className={reachableLevels.has(3) ? "text-green-400" : "text-neutral-600"}>
             ├─[L3] Clinical Division
          </div>
          <div className="pl-4 border-l border-neutral-700 ml-2">
            <div className={reachableLevels.has(5) ? "text-green-400" : "text-neutral-600"}>
               ├─[L5] Ortho Dept {result.entry_point === 'HL-05-ORTHO' ? '← ENTRY' : ''}
            </div>
            <div className="pl-4 border-l border-neutral-700 ml-2">
              <div className={reachableLevels.has(10) ? "text-green-400" : "text-neutral-600"}>
                 └─[L10] Ortho Ward {result.entry_point === 'HL-10-ORTHO-W' ? '← ENTRY' : ''}
              </div>
            </div>
            <div className={reachableLevels.has(5) ? "text-green-400" : "text-neutral-600"}>
               └─[L5] Medicine Dept
            </div>
          </div>
        </div>
        <div className="pl-4">
           <div className={reachableLevels.has(3) ? "text-green-400" : "text-neutral-600"}>
             └─[L3] Admin Division
           </div>
        </div>
        <div className="mt-4 pt-4 border-t border-neutral-800">
           <div className="text-blue-400">◆ [Zone 2] Global Constraints</div>
        </div>
        
        <div className="mt-6 flex gap-4 text-xs text-neutral-400">
          <span className="text-green-400">● Reachable</span>
          <span className="text-neutral-600">○ Not Reachable</span>
          <span className="text-blue-400">◆ Zone 2</span>
        </div>
      </div>
    </div>
  );
}
