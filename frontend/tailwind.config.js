const { theme } = require('./src/assets/theme');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: theme.colors.primary,
          light: theme.colors.light,
          dark: theme.colors.dark,
        },
        brand: {
          DEFAULT: theme.colors.brand,
        },
        background: theme.colors.background,
        surface: theme.colors.surface,
      },
      fontFamily: {
        sans: theme.fontFamily.sans,
      },
      maxWidth: {
        container: theme.spacing.container,
      },
    },
  },
  plugins: [],
};
