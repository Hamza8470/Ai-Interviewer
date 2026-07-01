import { useEffect, useRef, useState } from 'react';
import client from '../api/client';
import Sidebar from '../components/Sidebar';
import QuestionCard from '../components/QuestionCard';
import AudioPlayer from '../components/AudioPlayer';
import TranscriptBox from '../components/TranscriptBox';

export default function Interview() {
  const [session, setSession] = useState(null);
  const [length, setLength] = useState(5);
  const [company, setCompany] = useState('Amazon');
  const [role, setRole] = useState('React Developer');
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [result, setResult] = useState(null);
  const [audioSrc, setAudioSrc] = useState('');
  const [transcript, setTranscript] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const mediaRecorderRef = useRef(null);
  const mediaStreamRef = useRef(null);
  const chunksRef = useRef([]);

  const startInterview = async () => {
    setIsLoading(true);
    setError('');
    try {
      const response = await client.post('/interviews/start', { interview_length: length, company, role });
      setSession(response.data.interview);
      setResult(null);
      setTranscript('');
      setCurrentAnswer('');
      await speak(response.data.interview.questions?.[0]?.text);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Unable to start interview');
    } finally {
      setIsLoading(false);
    }
  };

  const speak = async (text) => {
    if (!text) return;
    setIsSpeaking(true);
    try {
      const formData = new FormData();
      formData.append('text', text);
      const response = await client.post('/voice/tts', formData, { responseType: 'blob' });
      const url = URL.createObjectURL(response.data);
      setAudioSrc(url);
    } finally {
      setIsSpeaking(false);
    }
  };

  const submitAnswer = async (answerText) => {
    if (!session?.questions?.[0]) return;
    setIsLoading(true);
    setError('');
    try {
      const response = await client.post('/interviews/answer', {
        interview_id: session.id,
        question_id: session.questions[0].id,
        answer: answerText || currentAnswer,
      });
      setResult(response.data);
      if (response.data.finished) {
        setSession(null);
        setCurrentAnswer('');
        return;
      }
      const nextQuestion = response.data.next_question;
      setSession((previous) => ({ ...previous, questions: [nextQuestion] }));
      setCurrentAnswer('');
      await speak(nextQuestion.text);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Unable to submit answer');
    } finally {
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      setError('');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStreamRef.current = stream;
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      chunksRef.current = [];
      recorder.ondataavailable = (event) => chunksRef.current.push(event.data);
      recorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        const file = new File([blob], 'answer.webm', { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('file', file);
        const response = await client.post('/voice/transcribe', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        setTranscript(response.data.transcript);
        setCurrentAnswer(response.data.transcript);
        setIsRecording(false);
      };
      recorder.start();
      setIsRecording(true);
    } catch (err) {
      setError('Microphone access is required for voice interviews');
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    mediaStreamRef.current?.getTracks().forEach((track) => track.stop());
  };

  useEffect(() => {
    if (session?.questions?.[0]?.text) {
      speak(session.questions[0].text);
    }
  }, [session]);

  useEffect(() => {
    return () => {
      mediaStreamRef.current?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  return (
    <main className="mx-auto grid max-w-7xl gap-6 px-4 py-10 lg:grid-cols-[280px_1fr] lg:px-8">
      <Sidebar />
      <section className="space-y-6">
        <div className="glass rounded-[2rem] p-8">
          <h1 className="text-3xl font-semibold text-white">Interview Session</h1>
          <p className="mt-2 text-slate-300">Question, answer, evaluation, next question, final report.</p>
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <label className="space-y-2 text-sm text-slate-300">
              <span>Length</span>
              <select value={length} onChange={(event) => setLength(Number(event.target.value))} className="w-full rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none">
                <option value={5}>5 Questions</option>
                <option value={10}>10 Questions</option>
              </select>
            </label>
            <label className="space-y-2 text-sm text-slate-300">
              <span>Company</span>
              <select value={company} onChange={(event) => setCompany(event.target.value)} className="w-full rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none">
                <option>Amazon</option>
                <option>Google</option>
                <option>Microsoft</option>
                <option>TCS</option>
                <option>Infosys</option>
                <option>Accenture</option>
              </select>
            </label>
            <label className="space-y-2 text-sm text-slate-300">
              <span>Role</span>
              <input value={role} onChange={(event) => setRole(event.target.value)} className="w-full rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none" placeholder="React Developer" />
            </label>
          </div>
          {error ? <div className="mt-4 rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</div> : null}
          {!session ? (
            <button onClick={startInterview} disabled={isLoading} className="mt-6 rounded-2xl bg-accent-500 px-5 py-3 font-semibold text-white hover:bg-accent-600 disabled:cursor-not-allowed disabled:opacity-60">
              {isLoading ? 'Starting...' : `Start ${length}-Question Interview`}
            </button>
          ) : (
            <div className="mt-6 space-y-4">
              <div className="flex flex-wrap items-center gap-3 text-sm text-slate-300">
                <span className="rounded-full border border-white/10 px-3 py-1">Current question: {session.current_question_index + 1} / {session.length}</span>
                <span className="rounded-full border border-white/10 px-3 py-1">Difficulty: {session.questions?.[0]?.difficulty || 'medium'}</span>
                <span className={`rounded-full px-3 py-1 ${isRecording ? 'bg-red-500/15 text-red-200' : 'border border-white/10'}`}>{isRecording ? 'Recording live' : 'Mic idle'}</span>
                <span className={`rounded-full px-3 py-1 ${isSpeaking ? 'bg-accent-500/15 text-accent-200' : 'border border-white/10'}`}>{isSpeaking ? 'Playing question audio' : 'Audio ready'}</span>
              </div>
              <div className="grid gap-4 xl:grid-cols-[1.3fr_0.7fr]">
                <QuestionCard question={session.questions?.[0]} index={session.current_question_index || 0} onAnswer={setCurrentAnswer} disabled={isLoading} />
                <div className="space-y-4">
                  <div className="glass rounded-3xl p-5">
                    <div className="text-sm text-slate-400">Session Controls</div>
                    <div className="mt-4 flex flex-wrap gap-3">
                      <button onClick={startRecording} disabled={isRecording || isLoading} className="rounded-2xl border border-white/10 px-4 py-2 text-white hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-60">Start Recording</button>
                      <button onClick={stopRecording} disabled={!isRecording} className="rounded-2xl border border-white/10 px-4 py-2 text-white hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-60">Stop Recording</button>
                      <button onClick={() => submitAnswer(currentAnswer)} disabled={isLoading} className="rounded-2xl bg-warm-500 px-4 py-2 font-semibold text-white hover:bg-warm-400 disabled:cursor-not-allowed disabled:opacity-60">{isLoading ? 'Submitting...' : 'Submit Answer'}</button>
                    </div>
                    <div className="mt-4 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-xs uppercase tracking-[0.3em] text-slate-400">
                      {session.current_question_index + 1 === session.length ? 'Final question path' : 'Adaptive follow-up enabled'}
                    </div>
                  </div>
                  <AudioPlayer src={audioSrc} />
                </div>
              </div>
              <TranscriptBox transcript={transcript} />
            </div>
          )}
        </div>
        {result ? (
          <div className="grid gap-4 lg:grid-cols-3">
            <div className="glass rounded-3xl p-5">
              <div className="text-sm text-slate-400">Technical Score</div>
              <div className="mt-2 text-4xl font-semibold text-white">{result.technical_score}</div>
              <div className="mt-2 text-sm text-slate-300">Evaluation is scored against the current answer and resume context.</div>
            </div>
            <div className="glass rounded-3xl p-5">
              <div className="text-sm text-slate-400">Communication Score</div>
              <div className="mt-2 text-4xl font-semibold text-white">{result.communication_score}</div>
              <div className="mt-2 text-sm text-slate-300">Voice answers are transcribed before scoring.</div>
            </div>
            <div className="glass rounded-3xl p-5">
              <div className="text-sm text-slate-400">Outcome</div>
              <div className="mt-2 text-2xl font-semibold text-white">{result.finished ? 'Interview completed' : 'Next question generated'}</div>
              <div className="mt-2 text-sm text-slate-300">{result.finished ? 'A PDF report has been generated and stored in reports.' : 'Continue to the next adaptive question.'}</div>
            </div>
            <div className="glass rounded-3xl p-5 lg:col-span-3">
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <div className="text-sm text-slate-400">Strengths</div>
                  <div className="mt-2 flex flex-wrap gap-2">{(result.evaluation?.strengths || []).map((item) => <span key={item} className="rounded-full border border-accent-500/30 bg-accent-500/10 px-3 py-1 text-sm text-accent-200">{item}</span>)}</div>
                </div>
                <div>
                  <div className="text-sm text-slate-400">Weaknesses</div>
                  <div className="mt-2 flex flex-wrap gap-2">{(result.evaluation?.weaknesses || []).map((item) => <span key={item} className="rounded-full border border-warm-500/30 bg-warm-500/10 px-3 py-1 text-sm text-warm-300">{item}</span>)}</div>
                </div>
              </div>
              <div className="mt-6 grid gap-4 md:grid-cols-2">
                <div>
                  <div className="text-sm text-slate-400">Feedback</div>
                  <div className="mt-2 text-slate-100">{result.evaluation?.feedback}</div>
                </div>
                <div>
                  <div className="text-sm text-slate-400">Suggested answer</div>
                  <div className="mt-2 text-slate-100">{result.evaluation?.correct_answer}</div>
                </div>
              </div>
            </div>
          </div>
        ) : null}
      </section>
    </main>
  );
}
