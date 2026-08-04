import { defineRouting } from 'next-intl/routing';

export const routing = defineRouting({
  locales: ['et-EE', 'en-US'],
  defaultLocale: 'et-EE',
  localePrefix: 'always',
});

export type Locale = (typeof routing.locales)[number];
