import { getTranslations } from 'next-intl/server';
import Header from '@/components/Header';
import type { Locale } from '@/i18n/routing';

export default async function HealthPage({
  params,
}: {
  params: Promise<{ locale: Locale }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'health' });

  return (
    <>
      <Header locale={locale} />
      <main>
        <h1>{t('title')}</h1>
        <p>{t('status.ok')}</p>
      </main>
    </>
  );
}
