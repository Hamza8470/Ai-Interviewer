import { useState } from 'react';
import client from '../api/client';
import FileUpload from '../components/FileUpload';

export default function ResumeUpload() {
  const [status, setStatus] = useState('');
  const [resume, setResume] = useState(null);

  const upload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    setStatus('Uploading...');
    const response = await client.post('/resumes/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
    setResume(response.data.resume);
    setStatus(response.data.message);
  };

  return (
    <main className="mx-auto max-w-4xl px-4 py-10 lg:px-8">
      <div className="glass rounded-[2rem] p-8">
        <h1 className="text-3xl font-semibold text-white">Resume Upload</h1>
        <p className="mt-2 text-slate-300">Upload a PDF resume to build your RAG knowledge base.</p>
        <div className="mt-6 space-y-4">
          <FileUpload onChange={upload} />
          {status ? <div className="text-sm text-accent-300">{status}</div> : null}
          {resume ? (
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-200">
              <div className="font-medium text-white">{resume.filename}</div>
              <div>Extracted text length: {resume.text_length}</div>
            </div>
          ) : null}
        </div>
      </div>
    </main>
  );
}
