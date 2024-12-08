const defaultTheme = require("tailwindcss/defaultTheme");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./core/templates/**/*.html",
    "./node_modules/flowbite/**/*.js",
    "./core/forms.py",
  ],
  theme: {
    fontFamily: {
      sans: ["Ysabeau Infant", ...defaultTheme.fontFamily.sans],
      serif: ["DM Serif Display", ...defaultTheme.fontFamily.serif],
      manrope: ["Manrope", ...defaultTheme.fontFamily.sans],
    },
    extend: {
      colors: {
        backgroundBlack: "#04070A",
        brand: "#D82336",
        brandBlack: "#101820",
        brandDark: "#08121C",
        brandGray: "#081D30",
        info: "#0094FF",
        secondary: "#FB7600",
        tertiary: "#826D61",
        "tertiary-400": "#826D61",
        success: "#00C136",
        warning: "#FA1616",
      },
      boxShadow: {
        'custom': '-2px 2px 21px -5px rgba(0, 0, 0, 0.75)',
      },
      keyframes: {
        opacity: {
          "0%": { opacity: 0 },
          "10%": { opacity: 0.1 },
          "20%": { opacity: 0.2 },
          "30%": { opacity: 0.3 },
          "40%": { opacity: 0.4 },
          "50%": { opacity: 0.5 },
          "60%": { opacity: 0.6 },
          "100%": { opacity: 1 },
        },
      },
      animation: {
        "opacity-in": "opacity 300ms linear",
      },
      maxWidth: {
        "screen-xs": "512px",
        "screen-2k": "1440px",
      },
      screens: {
        xs: "400px",
      },
      spacing: {
        '104': '28rem',
        '128': '32rem',
        '144': '36rem',
        '168': '48rem',
      },
      mode: 'jit',
      purge: ['./templates/**/*.html', './static/**/*.js'], // Adjust paths as needed
      theme: {
        extend: {},
      },
      plugins: [],
    },
  },
};
