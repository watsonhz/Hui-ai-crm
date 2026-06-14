// AI-CRM Service Worker v1.0 — 离线缓存策略
const CACHE = 'ai-crm-v1.0.0';
const ASSETS = ['/', '/dashboard', '/login', '/offline.html',
  '/customers', '/bidding', '/projects', '/relationships', '/contracts',
  '/ltc', '/acceptance', '/ai-reports', '/knowledge', '/settings', '/export'];

/** Install: 预缓存核心资源 */
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS).catch(() => {}))
  );
  self.skipWaiting();
});

/** Activate: 清理旧缓存 */
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

/** Fetch: 网络优先，失败时回退缓存 */
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        if (res.ok) {
          const clone = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, clone));
        }
        return res;
      })
      .catch(() => caches.match(e.request).then((cached) => cached || caches.match('/offline.html')))
  );
});

/** Push: 接收通知 */
self.addEventListener('push', (e) => {
  const data = e.data?.json() || { title: 'AI CRM', body: '新通知' };
  e.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/icons/icon-192.png',
      badge: '/icons/icon-192.png',
      tag: data.tag || 'default',
      data: data.url || '/',
    })
  );
});

/** 通知点击：打开对应页面 */
self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  e.waitUntil(
    self.clients.matchAll({ type: 'window' }).then((clients) => {
      const url = e.notification.data || '/';
      const client = clients.find((c) => c.url.includes(url));
      if (client) return client.focus();
      return self.clients.openWindow(url);
    })
  );
});
