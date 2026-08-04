'use client';

import { useTranslations } from 'next-intl';
import { useSearchParams } from 'next/navigation';
import { useRouter, usePathname } from '@/i18n/navigation';
import { routing } from '@/i18n/routing';
import type { Locale } from '@/i18n/routing';

const localeLabels: Record<string, string> = {
  'et-EE': 'et',
  'en-US': 'en',
};

export default function LanguageSwitcher({ locale }: { locale: Locale }) {
  const t = useTranslations('languageSwitcher');
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const otherLocale = routing.locales.find((l) => l !== locale) ?? routing.defaultLocale;

  const switchLanguage = () => {
    const searchString = searchParams?.toString() ?? '';
    const targetPath = searchString
      ? `${pathname}?${searchString}`
      : pathname;
    router.replace(targetPath, { locale: otherLocale });
  };

  return (
    <button onClick={switchLanguage} aria-label={t('label')} type="button">
      {t(localeLabels[otherLocale] ?? 'en')}
    </button>
  );
}
