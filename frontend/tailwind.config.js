/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Enable class-based dark mode
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        // Decent dark mode colors (muted, not full black)
        dark: {
          bg: '#1a1a2e', // Muted dark blue-gray
          surface: '#16213e', // Slightly lighter surface
          text: '#e2e8f0', // Light gray text
          border: '#2d3748', // Subtle border
          muted: '#4a5568', // Muted text
        }
      },
    },
  },
  plugins: [],
}