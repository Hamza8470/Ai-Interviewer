export default function FileUpload({ onChange, accept = '.pdf' }) {
  return (
    <input
      type="file"
      accept={accept}
      onChange={onChange}
      className="block w-full cursor-pointer rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200 file:mr-4 file:rounded-xl file:border-0 file:bg-accent-500 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-white hover:bg-white/8"
    />
  );
}
