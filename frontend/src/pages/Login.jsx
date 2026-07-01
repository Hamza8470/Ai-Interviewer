import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  const submit = async (event) => {
    event.preventDefault();
    try {
      await login(form.email, form.password);
      navigate('/dashboard');
    } catch (err) {
      setError(err?.response?.data?.detail || 'Unable to login');
    }
  };

  return (
    <main className="mx-auto flex min-h-[calc(100vh-80px)] max-w-md items-center px-4 py-10">
      <form onSubmit={submit} className="glass w-full rounded-[2rem] p-8">
        <h1 className="text-3xl font-semibold text-white">Login</h1>
        <p className="mt-2 text-sm text-slate-400">Access your interview workspace.</p>
        <div className="mt-6 space-y-4">
          <input className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none" placeholder="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none" placeholder="Password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
          {error ? <div className="rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</div> : null}
          <button className="w-full rounded-2xl bg-accent-500 px-4 py-3 font-semibold text-white hover:bg-accent-600">Login</button>
        </div>
        <p className="mt-6 text-sm text-slate-400">
          New here? <Link className="text-accent-300 hover:text-accent-200" to="/register">Create an account</Link>
        </p>
      </form>
    </main>
  );
}
