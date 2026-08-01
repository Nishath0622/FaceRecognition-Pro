/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#eefbf3',
          100: '#d5f5e0',
          200: '#aeecc4',
          300: '#7adda0',
          400: '#44c778',
          500: '#22ab5a',
          600: '#168b47',
          700: '#136f3a',
          800: '#125830',
          900: '#104929',
        }
      }
    }
  },
  plugins: [],
}
