// NovaGenAI Service Worker — fresh HTML + scoped offline caching
const CACHE_NAME = 'novagenai-v3';
const ASSETS = [
  '/',
  '/style.css',
  '/script.js',
  '/manifest.json',
  '/images/novagenai-logo-new.webp',
  '/images/favicon-64.png',
  '/images/apple-touch-icon.png',
  '/images/favicon.png',
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(key => key.startsWith('novagenai-') && key !== CACHE_NAME)
        .map(key => caches.delete(key))
    )).then(() => self.clients.claim())
  );
});

async function cacheResponse(cache, request, response) {
  if (response && response.status === 200 && response.type !== 'opaque') {
    await cache.put(request, response.clone()).catch(() => {});
  }
  return response;
}

self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;
  const isHtml = request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html');
  const isAsset = /\.(?:css|js|json|png|jpe?g|webp|svg|ico|woff2?)$/i.test(url.pathname);
  if (!isHtml && !isAsset) return;

  if (isHtml) {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE_NAME);
      try {
        return await cacheResponse(cache, request, await fetch(request, { cache: 'no-cache' }));
      } catch (error) {
        return await cache.match(request) || new Response(
          '<!doctype html><html lang="en"><meta name="viewport" content="width=device-width"><title>Offline — NovaGenAI</title><h1>You are offline</h1><p>This page is not saved offline. Please reconnect and reload.</p></html>',
          { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
        );
      }
    })());
    return;
  }

  const response = caches.open(CACHE_NAME).then(async cache => {
    const cached = await cache.match(request);
    const fresh = fetch(request).then(result => cacheResponse(cache, request, result))
      .catch(() => cached || Response.error());
    return { cached, fresh };
  });
  event.waitUntil(response.then(({ fresh }) => fresh).then(() => undefined));
  event.respondWith(response.then(({ cached, fresh }) => cached || fresh));
});
