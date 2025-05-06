/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  darkMode: 'class', // Enable dark mode manually
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb',     // blue-600
          light: '#3b82f6',       // blue-500
          dark: '#1e40af',        // blue-800
        },
        brand: {
          DEFAULT: '#0f172a',     // slate-900
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
