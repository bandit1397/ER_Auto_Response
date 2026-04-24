self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

// 푸시 알림
self.addEventListener('push', function(event) {
  const data = event.data ? event.data.json() : {};

  self.registration.showNotification("🚑 응급환자 요청", {
    body: data.message || "새 요청이 도착했습니다.",
    icon: "/icon.png",
    vibrate: [200,100,200],
    requireInteraction: true
  });
});
