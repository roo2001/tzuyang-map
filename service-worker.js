const CACHE_NAME = 'tzuyang-food-map-v3';
const ASSETS_TO_CACHE = [
  'index.html',
  'manifest.json',
  'icon.png',
  'tzuyang_restaurants_coords.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS_TO_CACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // HTML 대시보드와 데이터 JSON에 대해서는 Network-First 전략 적용 (캐시 고착 방지)
  if (url.pathname.includes('index.html') || url.pathname.includes('tzuyang_restaurants_coords.json')) {
    event.respondWith(
      fetch(event.request)
        .then(networkResponse => {
          if (networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseClone));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(event.request);
        })
    );
  } else {
    // 기타 이미지, 매니페스트 등 정적 자산은 Stale-While-Revalidate 활용
    event.respondWith(
      caches.match(event.request)
        .then(cachedResponse => {
          if (cachedResponse) {
            fetch(event.request).then(networkResponse => {
              if (networkResponse.status === 200) {
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, networkResponse));
              }
            });
            return cachedResponse;
          }
          return fetch(event.request);
        })
    );
  }
});
