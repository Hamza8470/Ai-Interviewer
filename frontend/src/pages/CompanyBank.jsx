import { useEffect, useState } from 'react';
import client from '../api/client';
import Sidebar from '../components/Sidebar';

export default function CompanyBank() {
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    client.get('/questions/bank').then((response) => setQuestions(response.data.questions || []));
  }, []);

  return (
    <main className="mx-auto grid max-w-7xl gap-6 px-4 py-10 lg:grid-cols-[280px_1fr] lg:px-8">
      <Sidebar />
      <section className="space-y-6">
        <div className="glass rounded-[2rem] p-8">
          <h1 className="text-3xl font-semibold text-white">Company Question Bank</h1>
          <p className="mt-2 text-slate-300">Amazon, Google, Microsoft, TCS, Infosys, and Accenture questions are available here.</p>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {questions.map((question, index) => (
            <div key={`${question.company}-${index}`} className="glass rounded-3xl p-5">
              <div className="text-xs uppercase tracking-[0.3em] text-slate-400">{question.company} | {question.difficulty} | {question.topic}</div>
              <div className="mt-2 text-white">{question.question}</div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
