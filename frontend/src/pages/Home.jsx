import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <main className="mx-auto grid max-w-7xl gap-10 px-4 py-20 lg:grid-cols-2 lg:px-8 lg:py-28">
      <section className="space-y-8">
        <div className="inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300">
          Agentic RAG-based mock interviews for modern hiring
        </div>
        <div className="space-y-4">
          <h1 className="max-w-xl text-5xl font-semibold tracking-tight text-white lg:text-7xl">
            AI Interviewer 5.0
          </h1>
          <p className="max-w-xl text-lg leading-8 text-slate-300">
            Upload a resume, generate personalized questions with Gemini, evaluate answers, adapt difficulty in real time, and export a professional interview report.
          </p>
        </div>
        <div className="flex flex-wrap gap-4">
          <Link to="/register" className="rounded-full bg-accent-500 px-6 py-3 font-semibold text-white shadow-lg shadow-accent-500/20 transition hover:bg-accent-600">
            Get Started
          </Link>
          <Link to="/login" className="rounded-full border border-white/10 px-6 py-3 font-semibold text-white transition hover:bg-white/10">
            Sign In
          </Link>
        </div>
      </section>
      <section className="glass rounded-[2rem] p-6 shadow-glow">
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="rounded-3xl bg-white/5 p-5">
            <div className="text-sm text-slate-400">Resume RAG</div>
            <div className="mt-2 text-2xl font-semibold text-white">FAISS + MiniLM</div>
          </div>
          <div className="rounded-3xl bg-white/5 p-5">
            <div className="text-sm text-slate-400">AI Scoring</div>
            <div className="mt-2 text-2xl font-semibold text-white">Gemini feedback</div>
          </div>
          <div className="rounded-3xl bg-white/5 p-5">
            <div className="text-sm text-slate-400">Voice</div>
            <div className="mt-2 text-2xl font-semibold text-white">Whisper + gTTS</div>
          </div>
          <div className="rounded-3xl bg-white/5 p-5">
            <div className="text-sm text-slate-400">Reports</div>
            <div className="mt-2 text-2xl font-semibold text-white">PDF export</div>
          </div>
        </div>
      </section>
    </main>
  );
}
