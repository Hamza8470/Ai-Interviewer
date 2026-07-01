export default function TranscriptBox({ transcript }) {
  if (!transcript) return null;
  return <div className="glass rounded-3xl p-5 text-sm text-slate-200">{transcript}</div>;
}
