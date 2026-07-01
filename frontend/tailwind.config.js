/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: {
          900: '#081120',
          800: '#0f172a',
          700: '#1e293b',
        },
        accent: {
          500: '#22c55e',
          600: '#16a34a',
        },
        warm: {
          400: '#f59e0b',
          500: '#f97316',
        },
      },
      boxShadow: {
        glow: '0 20px 60px rgba(34, 197, 94, 0.15)',
      },
      backgroundImage: {
        hero: 'radial-gradient(circle at top left, rgba(34,197,94,0.25), transparent 35%), radial-gradient(circle at right, rgba(249,115,22,0.18), transparent 30%), linear-gradient(135deg, #081120 0%, #0f172a 50%, #111827 100%)',
      },
    },
  },
  plugins: [],
};
