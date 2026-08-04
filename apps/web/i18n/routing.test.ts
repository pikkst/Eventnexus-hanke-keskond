import { describe, it, expect } from 'vitest';
import { routing } from '@/i18n/routing';
import etMessages from '@/messages/et-EE.json';
import enMessages from '@/messages/en-US.json';

describe('i18n configuration', () => {
  it('has et-EE as default locale', () => {
    expect(routing.defaultLocale).toBe('et-EE');
  });

  it('includes both locales', () => {
    expect(routing.locales).toEqual(['et-EE', 'en-US']);
  });

  it('Estonian messages have common headings', () => {
    expect(etMessages.common).toBeDefined();
    expect(etMessages.common.appName).toBe('Eventnexus');
    expect(etMessages.common.navigation.home).toBe('Avaleht');
  });

  it('English messages have common headings', () => {
    expect(enMessages.common).toBeDefined();
    expect(enMessages.common.appName).toBe('Eventnexus');
    expect(enMessages.common.navigation.home).toBe('Home');
  });

  it('both message files have matching top-level keys', () => {
    const etKeys = Object.keys(etMessages).sort();
    const enKeys = Object.keys(enMessages).sort();
    expect(etKeys).toEqual(enKeys);
  });

  it('Estonian navigation has expected keys', () => {
    expect(etMessages.common.navigation).toHaveProperty('home');
    expect(etMessages.common.navigation).toHaveProperty('opportunities');
    expect(etMessages.common.navigation).toHaveProperty('about');
  });

  it('English navigation has expected keys', () => {
    expect(enMessages.common.navigation).toHaveProperty('home');
    expect(enMessages.common.navigation).toHaveProperty('opportunities');
    expect(enMessages.common.navigation).toHaveProperty('about');
  });
});
