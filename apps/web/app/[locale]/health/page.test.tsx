import { describe, it, expect } from 'vitest';
import { routing } from '@/i18n/routing';
import etMessages from '@/messages/et-EE.json';
import enMessages from '@/messages/en-US.json';

describe('HealthPage translations', () => {
  it('Estonian health page has correct title and status', () => {
    const health = etMessages.health;
    expect(health.title).toBe('Tervisekontroll');
    expect(health.status.ok).toBe('Kõik näitajad on tervislikud');
    expect(health.status.error).toBe('Avastati probleem');
  });

  it('English health page has correct title and status', () => {
    const health = enMessages.health;
    expect(health.title).toBe('Health Check');
    expect(health.status.ok).toBe('All systems operational');
    expect(health.status.error).toBe('An issue was detected');
  });

  it('health route exists in routing config', () => {
    expect(routing.locales).toContain('et-EE');
    expect(routing.locales).toContain('en-US');
  });

  it('both locales have health namespace with matching keys', () => {
    const etKeys = Object.keys(etMessages.health).sort();
    const enKeys = Object.keys(enMessages.health).sort();
    expect(etKeys).toEqual(enKeys);
  });
});
