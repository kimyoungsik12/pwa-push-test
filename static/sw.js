// Service Worker for Push Notifications

self.addEventListener('install', (event) => {
    console.log('Service Worker 설치됨');
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('Service Worker 활성화됨');
    event.waitUntil(clients.claim());
});

self.addEventListener('push', (event) => {
    console.log('Push 이벤트 수신:', event);

    let notificationData = {
        title: '새로운 알림',
        body: '푸시 알림을 받았습니다.',
        icon: '/static/icon.png',
        badge: '/static/badge.png',
        vibrate: [200, 100, 200, 100, 200],  // 진동 패턴 강화
        tag: 'notification',
        requireInteraction: false,
        silent: false,  // 소리 활성화 (기본값이지만 명시)
        renotify: true  // 같은 tag의 알림도 소리/진동
    };

    if (event.data) {
        try {
            const data = event.data.json();
            notificationData = {
                ...notificationData,
                ...data
            };
        } catch (e) {
            console.error('Push 데이터 파싱 실패:', e);
        }
    }

    const promiseChain = self.registration.showNotification(
        notificationData.title,
        {
            body: notificationData.body,
            icon: notificationData.icon,
            badge: notificationData.badge,
            vibrate: notificationData.vibrate,
            tag: notificationData.tag,
            requireInteraction: notificationData.requireInteraction
        }
    );

    event.waitUntil(promiseChain);
});

self.addEventListener('notificationclick', (event) => {
    console.log('알림 클릭됨:', event);

    event.notification.close();

    event.waitUntil(
        clients.openWindow('/')
    );
});

self.addEventListener('notificationclose', (event) => {
    console.log('알림 닫힘:', event);
});
