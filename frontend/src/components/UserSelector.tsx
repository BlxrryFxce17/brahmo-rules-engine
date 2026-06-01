export default function UserSelector({ users, value, onChange }: { users: any[], value: string, onChange: (v: string) => void }) {
  return (
    <div className="flex flex-col min-w-[300px]">
      <label className="text-xs text-neutral-400 mb-1">Select User Profile</label>
      <select 
        value={value} 
        onChange={(e) => onChange(e.target.value)}
        className="bg-neutral-900 border border-neutral-700 text-white text-sm rounded-md focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5 outline-none"
      >
        <option value="">-- Choose User --</option>
        {users.map(u => (
          <option key={u.id} value={u.id}>
            {u.name} — {u.role}, L{u.ceiling_level} ({u.department})
          </option>
        ))}
      </select>
    </div>
  );
}
