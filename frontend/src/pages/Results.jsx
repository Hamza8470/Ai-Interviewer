import { useEffect, useState } from 'react';
import client from '../api/client';
import Sidebar from '../components/Sidebar';
import StatCard from '../components/StatCard';
import { TopicChart, TrendChart } from '../components/ScoreChart';

export default function Results() {
  const [reports, setReports] = useState([]);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    client.get('/reports').then((response) => setReports(response.data.reports || []));
    client.get('/analytics/dashboard').then((response) => setAnalytics(response.data));
  }, []);

  return (
    <main className="mx-auto grid max-w-7xl gap-6 px-4 py-10 lg:grid-cols-[280px_1fr] lg:px-8">
      <Sidebar />
      <section className="space-y-6">
        <div className="glass rounded-[2rem] p-8">
          <h1 className="text-3xl font-semibold text-white">Results</h1>
          <p className="mt-2 text-slate-300">Review completed interview reports, compare topic scores, and download polished PDF reports.</p>
        </div>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Total Interviews" value={analytics?.total_interviews ?? 0} />
          <StatCard label="Average Score" value={analytics?.average_score ?? 0} />
          <StatCard label="Strong Areas" value={analytics?.strong_areas?.length ?? 0} />
          <StatCard label="Weak Areas" value={analytics?.weak_areas?.length ?? 0} />
        </div>
        <div className="grid gap-6 xl:grid-cols-2">
          <TopicChart data={analytics?.topic_summary || []} />
          <TrendChart data={analytics?.improvement_trend || []} />
        </div>
        <div className="glass rounded-3xl p-5">
          <div className="mb-4 text-lg font-semibold text-white">Performance Notes</div>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <div className="text-sm text-slate-400">Strong Areas</div>
              <div className="mt-2 flex flex-wrap gap-2">
                {(analytics?.strong_areas || []).map((item) => (
                  <span key={item} className="rounded-full border border-accent-500/30 bg-accent-500/10 px-3 py-1 text-sm text-accent-200">
                    {item}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm text-slate-400">Weak Areas</div>
              <div className="mt-2 flex flex-wrap gap-2">
                {(analytics?.weak_areas || []).map((item) => (
                  <span key={item} className="rounded-full border border-warm-500/30 bg-warm-500/10 px-3 py-1 text-sm text-warm-300">
                    {item}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
        <div className="space-y-4">
          {reports.map((report) => (
            <div key={report.id} className="glass rounded-3xl p-5 shadow-glow">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <div className="text-lg font-semibold text-white">{report.company || 'General'}</div>
                  <div className="mt-1 text-sm text-slate-400">Technical {report.technical_score} | Communication {report.communication_score}</div>
                  <div className="mt-3 flex flex-wrap gap-2 text-xs uppercase tracking-[0.25em] text-slate-400">
                    <span className="rounded-full border border-white/10 px-3 py-1">Candidate report</span>
                    <span className="rounded-full border border-white/10 px-3 py-1">{new Date(report.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                <div className="flex flex-wrap gap-3">
                  <a className="rounded-2xl border border-white/10 px-4 py-2 text-white hover:bg-white/10" href={`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/reports/${report.id}/download`} target="_blank" rel="noreferrer">
                    Download PDF
                  </a>
                </div>
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-3">
                <div className="rounded-2xl bg-white/5 px-4 py-3 text-sm text-slate-200">
                  <div className="text-slate-400">Report ID</div>
                  <div className="mt-1 break-all">{report.id}</div>
                </div>
                <div className="rounded-2xl bg-white/5 px-4 py-3 text-sm text-slate-200">
                  <div className="text-slate-400">Interview ID</div>
                  <div className="mt-1 break-all">{report.interview_id}</div>
                </div>
                <div className="rounded-2xl bg-white/5 px-4 py-3 text-sm text-slate-200">
                  <div className="text-slate-400">Recommendation</div>
                  <div className="mt-1">Track weak topics in your next session.</div>
                </div>
              </div>
            </div>
          ))}
          {!reports.length ? <div className="glass rounded-3xl p-5 text-slate-300">No reports yet. Finish an interview to generate your first PDF report.</div> : null}
        </div>
      </section>
    </main>
  );
}
