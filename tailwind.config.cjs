/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");
module.exports = {
  content: ["./api/static/scripts/js/**/*.{ts,js}", "./api/templates/**/*.{html,js}", "./node_modules/flowbite/**/*.js", "./node_modules/tw-elements/js/**/*.js"],

  theme: {
    extend: {
      colors: {
        black: colors.black,
        white: colors.white,
        themecolor: "#913fe2",
      },
      fontFamily: {
        firasans: [
          "Fira Sans",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "system-ui",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "Noto Sans",
          "sans-serif",
          "Apple Color Emoji",
          "Segoe UI Emoji",
          "Segoe UI Symbol",
          "Noto Color Emoji",
        ],
      },
    },
  },
  darkMode: "class",
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
    require("tw-elements/plugin.cjs"),
    require("flowbite/plugin"),
    require("flowbite-typography"),
    require("daisyui"),
  ],
  daisyui: {},
};
