import type { ReactNode } from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import LanguageSwitcher from '@/components/LanguageSwitcher';
import { NextIntlClientProvider } from 'next-intl';

const etMessages = {
  languageSwitcher: {
    label: 'Vali keel',
    et: 'Eesti',
    en: 'Inglise',
  },
};

const enMessages = {
  languageSwitcher: {
    label: 'Select language',
    et: 'Estonian',
    en: 'English',
  },
};

const mockReplace = vi.fn();

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    replace: mockReplace,
    push: vi.fn(),
    refresh: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
  }),
  usePathname: () => '/opportunities/123',
  useSearchParams: () => new URLSearchParams('page=1'),
  redirect: vi.fn(),
  permanentRedirect: vi.fn(),
}));

function renderEt(ui: ReactNode) {
  return render(
    <NextIntlClientProvider locale="et-EE" messages={etMessages}>
      {ui}
    </NextIntlClientProvider>
  );
}

function renderEn(ui: ReactNode) {
  return render(
    <NextIntlClientProvider locale="en-US" messages={enMessages}>
      {ui}
    </NextIntlClientProvider>
  );
}

describe('LanguageSwitcher', () => {
  beforeEach(() => {
    mockReplace.mockClear();
  });

  it('renders English label when current locale is Estonian', () => {
    renderEt(<LanguageSwitcher locale="et-EE" />);
    const button = screen.getByRole('button', { name: 'Vali keel' });
    expect(button).toHaveTextContent('Inglise');
  });

  it('renders Estonian label when current locale is English', () => {
    renderEn(<LanguageSwitcher locale="en-US" />);
    const button = screen.getByRole('button', { name: 'Select language' });
    expect(button).toHaveTextContent('Estonian');
  });

  it('preserves current pathname and query when switching locale', () => {
    renderEt(<LanguageSwitcher locale="et-EE" />);
    const button = screen.getByRole('button');
    fireEvent.click(button);

    expect(mockReplace).toHaveBeenCalledTimes(1);
    const call = mockReplace.mock.calls[0];
    expect(call).toBeDefined();
    const targetPath = call![0] as string;
    expect(targetPath).toBe('/en-US/opportunities/123?page=1');
  });
});