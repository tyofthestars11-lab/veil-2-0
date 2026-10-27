const CACHE = 'crimson-desert-v1';
self.addEventListener('install', e => { self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(clients.claim()); });
self.addEventListener('fetch', e => {
  e.respondWith(
    caches.open(CACHE).then(c => c.match(e.request).then(hit => {
      const fetchPromise = fetch(e.request).then(res => {
        if (res && res.status === 200) c.put(e.request, res.clone());
        return res;
      }).catch(() => hit);
      return hit || fetchPromise;
    }))
  );
});
