const colors = require("tailwindcss/colors");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,jsx,ts,tsx}"],
  theme: {
    colors: {
      ...colors,
      blue: colors.blue,
      purple: colors.purple,
      pink: colors.pink,
      orange: colors.orange,
      green: colors.green,
      yellow: colors.yellow,
      grayDark: colors.gray[800],
      gray: colors.gray,
      grayLight: colors.gray[200],
    },
    fontFamily: {
      sans: ["Graphik", "sans-serif"],
      serif: ["Merriweather", "serif"],
    },
    extend: {
      spacing: {
        "8xl": "96rem",
        "9xl": "128rem",
      },
      borderRadius: {
        "4xl": "2rem",
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
