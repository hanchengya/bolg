/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#0F1419',
        'bg-secondary': '#1A1D29',
        'bg-tertiary': '#252A35',
        'accent-primary': '#FFB800',
        'accent-secondary': '#E50914',
      },
    },
  },
  plugins: [],
}

