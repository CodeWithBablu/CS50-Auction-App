/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./auctions/templates/**/*.html'],
  mode: "jit",
  theme: {
    extend: {
      gridTemplateColumns: {
        "auto-fit": "repeat(auto-fit,minmax(250px,270px))", //to automatic adjust grid layout
      },
      width: {
        150: "150px",
        190: "190px",
        225: "225px",
        275: "275px",
        300: "300px",
        340: "340px",
        350: "350px",
        375: "375px",
        460: "460px",
        656: "656px",
        880: "880px",
        508: "508px",
      },
      height: {
        80: "80px",
        150: "150px",
        225: "225px",
        300: "300px",
        340: "340px",
        370: "370px",
        420: "420px",
        510: "510px",
        600: "600px",
        650: "650px",
        685: "685px",
        800: "800px",
      },

      colors: {
        primary: "#748CAB",
        secondary: "#3E5C76",
        blackAplha100: "rgba(0, 0, 0, 0.06)",
        blackAplha200: "rgba(0, 0, 0, 0.08)",
        blackAplha300: "rgba(0, 0, 0, 0.16)",
        blackAplha400: "rgba(0, 0, 0, 0.24)",
        blackAplha500: "rgba(0, 0, 0, 0.36)",
        blackAplha600: "rgba(0, 0, 0, 0.48)",
        blackAplha700: "rgba(0, 0, 0, 0.64)",
        blackAplha800: "rgba(0, 0, 0, 0.80)",
        blackAplha900: "rgba(0, 0, 0, 0.90)",
        grayAplha600: "rgba(255, 255, 255, 0.06)",
        success: "rgba(34, 197, 94, 0.16)",
        error: "rgba(239, 68, 68, 0.16)",
        info: "rgba(59, 130, 246, 0.16)",
        header: "rgba(255, 255, 255, 0.4)",
      },
      fontFamily: {
        poppins: ["Poppins", "sans-serif"],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
