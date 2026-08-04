'use client';

import { useTranslations } from 'next-intl';
import { useEffect } from 'react';

export default function GlobalError({
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
    <html>
      <head />
      <body>
        <h2>{t('title')}</h2>
        <p>{t('description')}</p>
        <button onClick={() => reset()}>{t('retry')}</button>
      </body>
    </html>
  );
}
