# 📱 Push Notification Test Server

Python Flask 기반 웹 푸시 알림 테스트 서버입니다. 같은 Wi-Fi 네트워크에서 iPhone Safari와 Android Chrome에서 푸시 알림을 테스트할 수 있습니다.

## ✨ 주요 기능

- ✅ **iPhone Safari** 푸시 알림 지원 (iOS 16.4+)
- ✅ **Android Chrome** 푸시 알림 지원
- ✅ **HTTPS** 로컬 네트워크 지원 (자체 서명 인증서)
- ✅ **중복 구독 방지** (같은 기기에서 여러 번 구독해도 알림 1번)
- ✅ **구독 정보 영구 저장** (서버 재시작 시 유지)
- ✅ **커스텀 알림** (제목, 내용 변경 가능)
- ✅ **실시간 로그** (디버깅 편의성)

---

## 📋 필수 요구사항

### 서버 (노트북/PC)
- Python 3.8 이상
- 같은 Wi-Fi 네트워크

### 클라이언트
**iPhone:**
- iOS 16.4 이상
- Safari 브라우저
- 홈 화면 추가 필수 (PWA)

**Android:**
- Chrome, Firefox, Edge, Samsung Internet
- 홈 화면 추가 선택사항

---

## 🚀 빠른 시작 (3단계)

### 1단계: 의존성 설치
```bash
pip install -r requirements.txt
```

### 2단계: SSL 인증서 생성
```bash
python generate_cert.py
```

출력 예시:
```
🔒 SSL 인증서 생성 중...
📍 호스트명: DESKTOP-ABC123
📍 로컬 IP: 192.168.0.42
✅ SSL 인증서 생성 완료!
```

**참고:** VAPID 키는 이미 `app.py`에 포함되어 있어 별도 생성 불필요합니다.

### 3단계: 서버 실행
```bash
python app.py
```

출력 예시:
```
============================================================
🚀 Push Notification Test Server (HTTPS)
============================================================

📍 로컬 네트워크 주소: https://192.168.0.42:5000
📍 로컬호스트: https://localhost:5000

💡 iPhone Safari 접속 방법:
   1. Safari에서 https://192.168.0.42:5000 접속
   2. '이 연결은 비공개 연결이 아닙니다' → '자세히 보기' → '웹 사이트 방문'
   3. 홈 화면에 추가 (공유 버튼 → 홈 화면에 추가)
   4. 홈 화면 아이콘으로 실행

============================================================
```

---

## 📱 iPhone Safari 사용 방법

### 1단계: Safari에서 접속
```
https://192.168.0.42:5000
```
(위에서 확인한 IP 주소 사용)

### 2단계: 인증서 경고 무시
1. "이 연결은 비공개 연결이 아닙니다" 화면
2. **"자세히 보기"** 탭
3. **"웹 사이트 방문"** 탭

### 3단계: 홈 화면에 추가 ⭐ 필수!
1. Safari 하단 **공유 버튼(↑)** 탭
2. 스크롤해서 **"홈 화면에 추가"** 선택
3. **"추가"** 탭

### 4단계: Safari 완전히 닫기
- 홈 버튼 두 번 클릭 (또는 아래에서 위로 스와이프)
- Safari 앱을 **위로 밀어서 종료**

### 5단계: 홈 화면 아이콘으로 실행
- 홈 화면에서 **"Push Test"** 아이콘 탭
- ⚠️ Safari 브라우저가 아닌 독립 앱으로 실행되어야 함!

### 6단계: 알림 구독
1. **"알림 구독하기"** 버튼 탭
2. 알림 권한 요청 → **"허용"** 선택
3. "푸시 알림이 구독되어 있습니다" 메시지 확인

### 7단계: 푸시 알림 테스트
1. 알림 제목/내용 입력 (선택)
2. **"푸시 알림 전송"** 버튼 탭
3. iPhone 화면 상단에 알림 표시! 🎉

---

## 🤖 Android Chrome 사용 방법

Android는 iPhone보다 간단합니다!

### 1단계: Chrome 플래그 활성화 (자체 서명 인증서 허용)
```
1. Chrome 주소창에 입력: chrome://flags
2. 검색창에 입력: insecure
3. "Insecure origins treated as secure" 찾기
4. Disabled → Enabled 변경
5. 텍스트 박스에 입력: https://192.168.0.42:5000
6. 하단 "Relaunch" 버튼 클릭
```

### 2단계: 사이트 접속
```
https://192.168.0.42:5000
```

### 3단계: 인증서 경고 무시
"계속" 또는 "고급" → "안전하지 않음으로 이동" 클릭

### 4단계: 알림 구독 및 테스트
1. "알림 구독하기" 클릭
2. 권한 허용
3. "푸시 알림 전송" 클릭
4. 알림 수신! 🎉

**참고:** Android는 홈 화면 추가 없이 브라우저에서 바로 작동합니다!

---

## 🎵 알림 소리 설정

### iPhone
Web Push 알림 소리는 시스템 설정에 따라 결정됩니다.

**소리 활성화 방법:**
```
1. iPhone 설정 열기
2. 알림 탭
3. 하단에서 "Push Test" 찾기
4. "소리" 옵션 켜기
5. 무음 모드 해제 (옆면 스위치 확인)
6. 방해 금지 모드 해제
```

### Android
- 자동으로 시스템 알림 소리 재생
- 설정 > 앱 > Chrome > 알림에서 조정 가능

---

## 🧹 중복 구독 관리

같은 기기에서 여러 번 홈 화면에 추가해도 **중복 방지 시스템**이 자동으로 처리합니다.

### 자동 중복 방지
- 같은 기기에서 재구독 시 기존 구독 업데이트
- 알림은 항상 한 번만 전송됨
- 다른 기기는 각각 별도로 구독됨

### 수동 중복 정리 (필요시)
노트북 브라우저에서:
```
https://localhost:5000/static/cleanup_duplicates.html
```

"중복 제거 실행" 버튼 클릭 → 기존 중복 구독 자동 정리

---

## 🔧 트러블슈팅

### ❌ Service Worker 등록 실패

**증상:** "Service Worker를 지원하지 않는 브라우저입니다"

**해결:**

**iPhone:**
1. **홈 화면 추가 확인**
   - Safari 브라우저가 아닌 홈 화면 아이콘으로 실행했는지 확인
   - 화면 하단 로그: "독립 실행 모드: 예"로 표시되어야 함

2. **iOS 버전 확인**
   - iOS 16.4 이상 필요
   - 설정 > 일반 > 정보에서 확인

3. **Safari 완전히 종료 후 재시도**
   - 앱 전환기에서 Safari 위로 스와이프
   - 홈 화면 아이콘으로 다시 실행

**Android:**
1. **Chrome 플래그 확인**
   - `chrome://flags` → "Insecure origins treated as secure" 활성화
   - 정확한 IP 주소 입력 (https:// 포함)
   - Chrome 재시작

2. **캐시 삭제**
   - Chrome 메뉴(⋮) → 설정 → 개인정보 보호
   - 인터넷 사용 기록 삭제 → 캐시 및 쿠키 삭제

3. **시크릿 모드로 테스트**
   - Chrome 시크릿 탭에서 접속하여 캐시 영향 배제

---

### ❌ Push API 미지원

**증상:** "Push API를 지원하지 않는 브라우저입니다"

**iPhone:**
- 홈 화면 앱으로 실행 필수!
- Safari 브라우저 탭에서는 Push API 비활성화됨
- 화면 하단 로그에서 "독립 실행 모드" 확인

**Android:**
- Chrome 최신 버전으로 업데이트
- 브라우저 설정 > 사이트 설정 > 알림 허용 확인

---

### ❌ 알림이 오지 않음

**증상:** 구독은 성공했지만 알림이 표시되지 않음

**공통:**
1. **알림 권한 확인**
   - 설정 > 알림 > "Push Test" 또는 Chrome
   - 알림 허용 상태 확인

2. **방해 금지 모드 해제**
   - iPhone: 제어 센터에서 초승달 아이콘 확인
   - Android: 설정 > 소리 및 진동

3. **서버 로그 확인**
   - 노트북 터미널에서 "📤 푸시 전송 성공" 메시지 확인
   - 에러 메시지가 있다면 복사하여 분석

**iPhone 전용:**
- 무음 모드 해제 (옆면 스위치, 주황색 표시 안 보이게)
- 설정 > 알림 > "Push Test" > 소리 활성화

---

### ❌ 연결 시간 초과

**증상:** iPhone/Android에서 사이트 접속 불가

**해결:**
1. **같은 Wi-Fi 확인**
   - 노트북과 모바일 기기가 동일한 Wi-Fi에 연결되어 있는지 확인
   - 게스트 네트워크는 기기 간 통신이 차단될 수 있음

2. **IP 주소 재확인**
   ```bash
   ipconfig  # Windows
   ifconfig  # macOS/Linux
   ```
   - 무선 LAN 어댑터의 IPv4 주소 사용
   - 예: 192.168.0.42

3. **방화벽 확인**
   - Windows: Windows Defender 방화벽 → "앱이 방화벽을 통과하도록 허용"
   - Python 항목에서 "개인" 체크

4. **서버 실행 확인**
   - 노트북 브라우저에서 `https://localhost:5000` 접속
   - 정상 작동하면 서버는 문제없음

---

### ❌ HTTPS 인증서 에러

**증상:** "인증서가 유효하지 않습니다"

**해결:**
- 로컬 테스트용 자체 서명 인증서는 정상입니다
- "자세히 보기" → "웹 사이트 방문" 클릭하여 계속 진행
- 보안 경고는 예상된 동작입니다

---

### ❌ cryptography 라이브러리 에러

**증상:** `TypeError: curve must be an EllipticCurve instance`

**해결:**
```bash
pip install cryptography==41.0.7
```

---

## 📂 프로젝트 구조

```
.
├── app.py                          # Flask 서버 메인 파일
├── generate_cert.py                # SSL 인증서 생성 스크립트
├── setup.py                        # VAPID 키 생성 및 설정 (선택)
├── requirements.txt                # Python 의존성
├── subscriptions.json              # 구독 정보 저장 (자동 생성)
├── cert.pem                        # SSL 인증서 (자동 생성)
├── key.pem                         # SSL 개인키 (자동 생성)
├── templates/
│   └── index.html                 # 프론트엔드 UI
├── static/
│   ├── sw.js                      # Service Worker
│   ├── manifest.json              # PWA Manifest
│   └── cleanup_duplicates.html    # 중복 정리 도구
├── README.md                       # 이 파일
└── ANDROID_SETUP.md               # 안드로이드 상세 설정 가이드
```

---

## 🔑 주요 API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 메인 페이지 |
| `GET` | `/sw.js` | Service Worker 파일 |
| `GET` | `/vapid-public-key` | VAPID 공개키 조회 |
| `POST` | `/subscribe` | 푸시 알림 구독 등록/업데이트 |
| `POST` | `/unsubscribe` | 푸시 알림 구독 해제 |
| `POST` | `/send-notification` | 모든 구독자에게 푸시 알림 전송 |
| `POST` | `/cleanup-duplicates` | 중복 구독 제거 |
| `GET` | `/test-notification` | 첫 번째 구독자에게 테스트 알림 전송 |

---

## 💾 데이터 저장

### subscriptions.json
구독 정보가 자동으로 파일에 저장됩니다.

```json
[
  {
    "endpoint": "https://fcm.googleapis.com/fcm/send/...",
    "keys": {
      "p256dh": "...",
      "auth": "..."
    }
  }
]
```

**특징:**
- 서버 재시작 시 자동으로 로드
- 구독/해제 시 실시간 저장
- 중복 구독 자동 방지

**초기화 방법:**
```bash
# subscriptions.json 파일 삭제
rm subscriptions.json  # macOS/Linux
del subscriptions.json  # Windows
```

---

## ⚙️ 고급 설정

### VAPID 키 재생성 (선택)

기본 VAPID 키가 이미 포함되어 있지만, 원하면 새로 생성할 수 있습니다.

```bash
python setup.py
```

`app.py`의 `VAPID_PUBLIC_KEY`와 `VAPID_PRIVATE_KEY`가 자동으로 업데이트됩니다.

**주의:** VAPID 키를 변경하면 기존 구독이 무효화되므로 재구독 필요합니다.

---

### 포트 변경

`app.py` 마지막 부분 수정:
```python
app.run(
    host='0.0.0.0',
    port=8080,  # 원하는 포트
    ssl_context=('cert.pem', 'key.pem'),
    debug=True
)
```

---

### 프로덕션 배포

이 서버는 **테스트 목적**입니다. 프로덕션 환경에서는:

**필수 변경사항:**
- ✅ 정식 SSL 인증서 사용 (Let's Encrypt 등)
- ✅ 데이터베이스로 구독 관리 (PostgreSQL, MongoDB 등)
- ✅ 환경변수로 VAPID 키 관리
- ✅ Rate limiting 구현 (Flask-Limiter)
- ✅ 에러 처리 및 로깅 강화
- ✅ WSGI 서버 사용 (Gunicorn, uWSGI)
- ✅ 리버스 프록시 설정 (Nginx)

---

## 🌐 브라우저 호환성

| 플랫폼 | 브라우저 | 최소 버전 | 홈 화면 추가 |
|--------|----------|-----------|-------------|
| iOS | Safari | 16.4+ | ✅ 필수 |
| Android | Chrome | 42+ | ⚪ 선택 |
| Android | Firefox | 44+ | ⚪ 선택 |
| Android | Edge | 79+ | ⚪ 선택 |
| Android | Samsung Internet | 4.0+ | ⚪ 선택 |
| Desktop | Chrome | 42+ | ❌ 불필요 |
| Desktop | Firefox | 44+ | ❌ 불필요 |
| Desktop | Edge | 79+ | ❌ 불필요 |

**참고:**
- iPhone은 Safari만 지원 (Chrome, Firefox 등은 불가)
- Android는 대부분의 모던 브라우저 지원
- Desktop 브라우저는 개발/테스트 용도로 사용 가능

---

## 📚 참고 자료

### 공식 문서
- [iOS 16.4+ Web Push 소개](https://webkit.org/blog/13966/web-push-for-web-apps-on-ios-and-ipados/)
- [Web Push Protocol 명세](https://developers.google.com/web/fundamentals/push-notifications)
- [Service Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Push API 사양](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)

### 유용한 도구
- [VAPID Key Generator](https://web-push-codelab.glitch.me/)
- [Web Push Tester](https://tests.peter.sh/notification-generator/)
- [Can I Use - Push API](https://caniuse.com/push-api)

---


