import { Link } from 'react-router-dom';

const items = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/resume-upload', label: 'Resume Upload' },
  { to: '/interview', label: 'Interview' },
  { to: '/results', label: 'Results' },
  { to: '/profile', label: 'Profile' },
  { to: '/company-bank', label: 'Company Bank' },
];

export default function Sidebar() {
  return (
    <aside className="glass hidden h-fit rounded-3xl p-4 lg:block">
      <div className="mb-4 text-xs uppercase tracking-[0.3em] text-slate-400">Workspace</div>
      <div className="space-y-1">
        {items.map((item) => (
          <Link key={item.to} to={item.to} className="block rounded-2xl px-4 py-3 text-sm text-slate-200 transition hover:bg-white/8 hover:text-white">
            {item.label}
          </Link>
        ))}
      </div>
    </aside>
  );
}
