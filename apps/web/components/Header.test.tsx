import type { ReactNode } from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import Header from '@/components/Header';
import { NextIntlClientProvider } from 'next-intl';

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

const messages = {
  header: {
    logo: 'Eventnexus',
    menu: {
      home: 'Avaleht',
    },
  },
  languageSwitcher: {
    label: 'Vali keel',
    et: 'Eesti',
    en: 'Inglise',
  },
  common: {
    loading: 'Laadimine...',
  },
};

function renderWithProviders(ui: ReactNode, locale = 'et-EE') {
  return render(
    <NextIntlClientProvider locale={locale} messages={messages}>
      {ui}
    </NextIntlClientProvider>
  );
}

describe('Header', () => {
  it('renders home link with correct text', () => {
    renderWithProviders(<Header locale="et-EE" />);
    const homeLink = screen.getByText('Avaleht');
    expect(homeLink).toBeInTheDocument();
  });

  it('renders the logo', () => {
    renderWithProviders(<Header locale="et-EE" />);
    const logo = screen.getByText('Eventnexus');
    expect(logo).toBeInTheDocument();
  });
});
