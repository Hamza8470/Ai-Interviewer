import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-20 border-b border-white/10 bg-slate-950/70 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 lg:px-8">
        <Link to="/" className="text-lg font-semibold tracking-tight text-white">
          AI Interviewer 5.0
        </Link>
        <nav className="flex items-center gap-3 text-sm text-slate-300">
          <Link to="/dashboard" className="hover:text-white">Dashboard</Link>
          <Link to="/resume-upload" className="hover:text-white">Resume</Link>
          <Link to="/interview" className="hover:text-white">Interview</Link>
          <Link to="/results" className="hover:text-white">Results</Link>
          <Link to="/profile" className="hover:text-white">Profile</Link>
          {user ? (
            <button onClick={handleLogout} className="rounded-full border border-white/10 px-4 py-2 text-white hover:bg-white/10">
              Logout
            </button>
          ) : (
            <Link to="/login" className="rounded-full border border-accent-500/40 px-4 py-2 text-accent-300 hover:bg-accent-500/10">
              Login
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
}
