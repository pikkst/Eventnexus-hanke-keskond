import { describe, it, expect } from 'vitest';
import { routing } from '@/i18n/routing';
import createMiddleware from 'next-intl/middleware';

describe('proxy / locale middleware', () => {
  it('routes config exports expected locales', () => {
    expect(routing.locales).toContain('et-EE');
    expect(routing.locales).toContain('en-US');
  });

  it('createMiddleware is exported from next-intl/middleware', () => {
    expect(typeof createMiddleware).toBe('function');
  });

  it('middleware type is function', () => {
    const middleware = createMiddleware(routing);
    expect(typeof middleware).toBe('function');
  });
});
