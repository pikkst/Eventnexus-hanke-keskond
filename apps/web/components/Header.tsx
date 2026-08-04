'use client';

import { useTranslations } from 'next-intl';
import LanguageSwitcher from './LanguageSwitcher';
import { Link } from '@/i18n/navigation';
import type { Locale } from '@/i18n/routing';

export default function Header({ locale }: { locale: Locale }) {
  const t = useTranslations('header');

  return (
    <header>
      <nav>
        <Link href="/">{t('logo')}</Link>
        <ul>
          <li>
            <Link href="/">{t('menu.home')}</Link>
          </li>
        </ul>
        <LanguageSwitcher locale={locale} />
      </nav>
    </header>
  );
}
