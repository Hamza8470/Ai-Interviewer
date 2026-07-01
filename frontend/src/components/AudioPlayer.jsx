export default function AudioPlayer({ src }) {
  if (!src) return null;
  return <audio className="w-full" controls autoPlay src={src} />;
}
