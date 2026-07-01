import { useEffect, useState } from 'react';
import client from '../api/client';
import Sidebar from '../components/Sidebar';
import StatCard from '../components/StatCard';
import { TopicChart, TrendChart } from '../components/ScoreChart';

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    client.get('/analytics/dashboard').then((response) => setData(response.data));
  }, []);

  return (
    <main className="mx-auto grid max-w-7xl gap-6 px-4 py-10 lg:grid-cols-[280px_1fr] lg:px-8">
      <Sidebar />
      <section className="space-y-6">
        <div className="glass rounded-[2rem] p-8">
          <h1 className="text-3xl font-semibold text-white">Dashboard</h1>
          <p className="mt-2 max-w-2xl text-slate-300">Track your progress, see recent reports, and review your strongest and weakest interview topics.</p>
        </div>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Total Interviews Taken" value={data?.total_interviews ?? 0} />
          <StatCard label="Average Score" value={data?.average_score ?? 0} />
          <StatCard label="Strong Areas" value={data?.strong_areas?.length ?? 0} />
          <StatCard label="Weak Areas" value={data?.weak_areas?.length ?? 0} />
        </div>
        <div className="grid gap-6 xl:grid-cols-2">
          <TopicChart data={data?.topic_summary || []} />
          <TrendChart data={data?.improvement_trend || []} />
        </div>
        <div className="glass rounded-3xl p-5">
          <div className="mb-4 text-lg font-semibold text-white">Recent Reports</div>
          <div className="space-y-3">
            {(data?.recent_reports || []).map((report) => (
              <div key={report.id} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200">
                <div className="font-medium text-white">{report.company || 'General'} interview</div>
                <div className="text-slate-400">Technical: {report.technical_score} | Communication: {report.communication_score}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
