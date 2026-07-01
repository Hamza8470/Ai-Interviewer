export default function QuestionCard({ question, index, onAnswer, disabled }) {
  return (
    <div className="glass rounded-3xl p-5">
      <div className="text-xs uppercase tracking-[0.3em] text-slate-400">Question {index + 1}</div>
      <h3 className="mt-2 text-xl font-semibold text-white">{question?.text}</h3>
      <p className="mt-2 text-sm text-slate-400">Difficulty: {question?.difficulty || 'medium'}</p>
      <textarea
        className="mt-4 min-h-40 w-full rounded-2xl border border-white/10 bg-slate-950/70 p-4 text-slate-100 outline-none placeholder:text-slate-500"
        placeholder="Type your answer here..."
        onBlur={(event) => onAnswer(event.target.value)}
        disabled={disabled}
      />
    </div>
  );
}
