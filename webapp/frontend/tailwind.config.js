/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
    colors: {
      primary: "#56876D",
      secondary: "#BDBEA9",
      information: "#04724D",
      success: "#8DB38B",
      warning: "#D2AB99",
    }
  },
  plugins: [],
}