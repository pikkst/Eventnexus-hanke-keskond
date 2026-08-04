import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';
import type { PluginOption } from 'vite';

export default defineConfig({
  plugins: [react() as PluginOption, tsconfigPaths() as PluginOption],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    include: ['**/*.{test,spec}.{ts,tsx}'],
    exclude: ['node_modules', '.next', 'build', 'dist'],
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      exclude: ['node_modules', '.next', 'build', 'dist', '**/*.d.ts', 'vitest.config.*'],
    },
    server: {
      deps: {
        inline: ['next-intl'],
      },
    },
  },
});
