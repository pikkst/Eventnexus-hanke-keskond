import { describe, it, expect, afterEach, beforeEach, vi } from 'vitest';

describe('health API route', () => {
  let originalDate: typeof Date;

  beforeEach(() => {
    originalDate = Date;
    const mockDate = new Date('2026-08-04T12:00:00.000Z');
    vi.useFakeTimers().setSystemTime(mockDate.getTime());
  });

  afterEach(() => {
    vi.useRealTimers();
    global.Date = originalDate;
  });

  it('returns ok status with timestamp', async () => {
    const { GET } = await import('@/app/api/health/route');
    const response = await GET();

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.status).toBe('ok');
    expect(data.timestamp).toBe('2026-08-04T12:00:00.000Z');
  });
});
