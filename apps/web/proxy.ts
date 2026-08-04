import createMiddleware from 'next-intl/middleware';
import type { NextRequest } from 'next/server';
import { routing } from '@/i18n/routing';

export const config = {
  matcher: [
    '/((?!api|_next|.*\\..*).*)',
  ],
};

const middleware = createMiddleware(routing);

export default async function proxy(request: NextRequest) {
  return middleware(request);
}
