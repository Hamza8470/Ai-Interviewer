export default function StatCard({ label, value, hint }) {
  return (
    <div className="glass rounded-3xl p-5 shadow-glow">
      <div className="text-sm text-slate-400">{label}</div>
      <div className="mt-2 text-3xl font-semibold text-white">{value}</div>
      {hint ? <div className="mt-2 text-sm text-slate-300">{hint}</div> : null}
    </div>
  );
}
