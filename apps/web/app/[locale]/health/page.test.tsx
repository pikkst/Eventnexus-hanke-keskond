import type { ReactNode } from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import HealthPage from '@/app/[locale]/health/page';
import { NextIntlClientProvider } from 'next-intl';
import etMessages from '@/messages/et-EE.json';
import enMessages from '@/messages/en-US.json';
import { routing } from '@/i18n/routing';

vi.mock('next-intl/server', () => ({
  getTranslations: (opts: { locale: string; namespace?: string }) => {
    const messages = opts.locale === 'et-EE' ? etMessages : enMessages;
    const ns = opts.namespace;
    const root = ns ? (messages as Record<string, Record<string, unknown>>)[ns] : messages;
    return (key: string) => {
      const parts = key.split('.');
      let obj: unknown = root;
      for (const p of parts) {
        obj = (obj as Record<string, unknown>)[p];
      }
      return obj as string;
    };
  },
}));

vi.mock('@/components/Header', () => ({
  default: () => null,
}));

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    replace: vi.fn(),
    push: vi.fn(),
    refresh: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
  }),
  usePathname: () => '/',
  useSearchParams: () => null,
  redirect: vi.fn(),
  permanentRedirect: vi.fn(),
}));

function renderWithProviders(ui: ReactNode, locale: string, messages: Record<string, unknown>) {
  return render(
    <NextIntlClientProvider locale={locale} messages={messages}>
      {ui}
    </NextIntlClientProvider>
  );
}

describe('HealthPage', () => {
  it('renders Estonian health page content', async () => {
    const page = await HealthPage({ params: Promise.resolve({ locale: 'et-EE' }) });
    renderWithProviders(page, 'et-EE', etMessages);
    expect(screen.getByRole('heading', { level: 1, name: 'Tervisekontroll' })).toBeInTheDocument();
    expect(screen.getByText('Kõik näitajad on tervislikud')).toBeInTheDocument();
  });

  it('renders English health page content', async () => {
    const page = await HealthPage({ params: Promise.resolve({ locale: 'en-US' }) });
    renderWithProviders(page, 'en-US', enMessages);
    expect(screen.getByRole('heading', { level: 1, name: 'Health Check' })).toBeInTheDocument();
    expect(screen.getByText('All systems operational')).toBeInTheDocument();
  });

  it('Estonian and English health messages have matching keys', () => {
    const etKeys = Object.keys(etMessages.health).sort();
    const enKeys = Object.keys(enMessages.health).sort();
    expect(etKeys).toEqual(enKeys);
  });

  it('includes both locales in routing config', () => {
    expect(routing.locales).toContain('et-EE');
    expect(routing.locales).toContain('en-US');
  });
});
