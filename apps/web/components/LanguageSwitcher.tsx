'use client';

import { useRouter } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { routing } from '@/i18n/routing';
import type { Locale } from '@/i18n/routing';

const localeLabels: Record<string, string> = {
  'et-EE': 'et',
  'en-US': 'en',
};

export default function LanguageSwitcher({ locale }: { locale: Locale }) {
  const router = useRouter();
  const t = useTranslations('languageSwitcher');
  const otherLocale = routing.locales.find((l) => l !== locale) ?? routing.defaultLocale;

  const switchLanguage = () => {
    router.replace(`/${otherLocale}/`);
  };

  return (
    <button onClick={switchLanguage} aria-label={t('label')} type="button">
      {t(localeLabels[otherLocale] ?? 'en')}
    </button>
  );
}
