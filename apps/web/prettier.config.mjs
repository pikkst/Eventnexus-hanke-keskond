/** @type {import('prettier').Config} */
const config = {
  printWidth: 100,
  tabWidth: 2,
  useTabs: false,
  semi: true,
  singleQuote: true,
  trailingComma: 'all',
  bracketSpacing: true,
  arrowParens: 'all',
  endOfLine: 'lf',
  overrides: [
    {
      files: ['*.md', '*.json'],
      tabWidth: 2,
      singleQuote: false,
    },
  ],
};

export default config;
