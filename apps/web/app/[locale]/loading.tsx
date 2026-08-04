import { useTranslations } from 'next-intl';

export default function Loading() {
  const t = useTranslations('common');
  return <div>{t('loading')}</div>;
}
