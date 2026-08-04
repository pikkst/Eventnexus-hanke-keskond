import '@/app/globals.css';

import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { NextIntlClientProvider } from 'next-intl';
import { getTranslations } from 'next-intl/server';
import { getMessages } from 'next-intl/server';
import { locale as getLocaleParam } from 'next/root-params';
import { routing } from '@/i18n/routing';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'metadata' });
  return {
    title: {
      default: t('title'),
      template: `%s | ${t('title')}`,
    },
    description: t('description'),
    alternates: {
      languages: Object.fromEntries(routing.locales.map((loc) => [loc, `/${loc}`])),
    },
  };
}

export default async function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  const currentLocale = await getLocaleParam();
  const messages = await getMessages({ locale: currentLocale });

  return (
    <html lang={currentLocale}>
      <head />
      <body>
        <NextIntlClientProvider locale={currentLocale} messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
