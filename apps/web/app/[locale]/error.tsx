'use client';

import { useTranslations } from 'next-intl';
import { useEffect } from 'react';

export default function LocaleError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const t = useTranslations('error');

  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <section>
      <h2>{t('title')}</h2>
      <p>{t('description')}</p>
      <button onClick={() => reset()}>{t('retry')}</button>
    </section>
  );
}
