import { useEffect, useState } from 'react';
import client from '../api/client';
import Sidebar from '../components/Sidebar';
import { useAuth } from '../context/AuthContext';

export default function Profile() {
  const { user, setUser } = useAuth();
  const [form, setForm] = useState({ name: '', target_role: '', experience_level: '', company_target: '' });

  useEffect(() => {
    if (user) {
      setForm({
        name: user.name || '',
        target_role: user.target_role || '',
        experience_level: user.experience_level || '',
        company_target: user.company_target || '',
      });
    }
  }, [user]);

  const save = async () => {
    const payload = { ...form };
    const response = await client.patch('/auth/me', payload).catch(() => null);
    if (response?.data) setUser(response.data);
  };

  return (
    <main className="mx-auto grid max-w-7xl gap-6 px-4 py-10 lg:grid-cols-[280px_1fr] lg:px-8">
      <Sidebar />
      <section className="space-y-6">
        <div className="glass rounded-[2rem] p-8">
          <h1 className="text-3xl font-semibold text-white">Profile</h1>
          <p className="mt-2 text-slate-300">Update your interview preferences.</p>
        </div>
        <div className="glass rounded-3xl p-6 space-y-4">
          <input className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Name" />
          <input className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white" value={form.target_role} onChange={(e) => setForm({ ...form, target_role: e.target.value })} placeholder="Target role" />
          <input className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white" value={form.experience_level} onChange={(e) => setForm({ ...form, experience_level: e.target.value })} placeholder="Experience level" />
          <input className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white" value={form.company_target} onChange={(e) => setForm({ ...form, company_target: e.target.value })} placeholder="Target company" />
          <button onClick={save} className="rounded-2xl bg-accent-500 px-5 py-3 font-semibold text-white hover:bg-accent-600">Save Profile</button>
        </div>
      </section>
    </main>
  );
}
