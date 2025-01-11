/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Ensures all React components are scanned for Tailwind classes
    "./public/index.html",
  ],
  theme: {
    extend: {}, // Use this section for custom theming if needed
  },
  plugins: [], // Add TailwindCSS plugins here if required
};
