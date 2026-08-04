import nextConfig from 'eslint-config-next';
import tseslint from 'typescript-eslint';

const config = [
  ...nextConfig,
  ...tseslint.configs.recommended,
  {
    name: 'eventnexus/web',
    rules: {
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
      ],
    },
  },
];

export default config;
