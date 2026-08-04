import { getRequestConfig } from 'next-intl/server';
import { hasLocale } from 'use-intl';
import { routing } from '@/i18n/routing';
import type { Locale } from '@/i18n/routing';

export default getRequestConfig(async ({ requestLocale }) => {
  let locale: Locale;
  const requested = await requestLocale;
  if (requested && hasLocale(routing.locales, requested)) {
    locale = requested as Locale;
  } else {
    locale = routing.defaultLocale;
  }

  return {
    locale,
    messages: (await import(`@/messages/${locale}.json`)).default,
  };
});
