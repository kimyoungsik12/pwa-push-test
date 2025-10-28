# 안드로이드 Chrome에서 테스트하기

안드로이드에서 자체 서명 인증서를 사용한 Service Worker를 등록하려면 추가 설정이 필요합니다.

## 방법 1: Chrome 플래그 활성화 (가장 빠름)

### 단계별 설정:

1. **Chrome에서 플래그 페이지 열기**
   ```
   chrome://flags
   ```
   주소창에 입력

2. **"Insecure origins" 검색**
   검색창에 `insecure` 입력

3. **"Insecure origins treated as secure" 찾기**
   - **Disabled**로 되어있는 항목 찾기

4. **서버 주소 추가**
   - 드롭다운 클릭 → **Enabled** 선택
   - 텍스트 박스에 입력:
     ```
     https://192.168.0.42:5000
     ```
   - 정확한 IP 주소 사용!

5. **Chrome 재시작**
   - 하단에 나타나는 **"Relaunch"** 버튼 클릭

6. **테스트**
   ```
   https://192.168.0.42:5000
   ```
   접속 → Service Worker 등록 성공!

---

## 방법 2: 인증서 설치 (영구적)

자체 서명 인증서를 안드로이드에 신뢰할 수 있는 인증서로 설치합니다.

### 1단계: 인증서 파일 전송

**노트북에서:**
```bash
# cert.pem을 안드로이드로 전송
# 방법 1: 이메일로 자신에게 보내기
# 방법 2: USB 케이블로 복사
# 방법 3: 클라우드 드라이브 (Google Drive 등)
```

### 2단계: 안드로이드에서 설치

```
1. 설정 → 보안 → 암호화 및 자격 증명
2. "인증서 설치" 또는 "CA 인증서 설치"
3. 전송받은 cert.pem 파일 선택
4. 인증서 이름 입력 (예: "Push Test Local")
5. 확인
```

### 3단계: Chrome 재시작 후 테스트

---

## 방법 3: HTTP로 테스트 (테스트 목적만)

Service Worker는 HTTPS가 필요하지만, localhost는 예외입니다.

### Port Forwarding 사용:

**노트북에서:**
```bash
# ADB 설치 필요
adb reverse tcp:5000 tcp:5000
```

**안드로이드 Chrome에서:**
```
http://localhost:5000
```

이 경우 HTTP여도 Service Worker가 작동합니다!

---

## 추천 방법

**빠른 테스트:** 방법 1 (Chrome 플래그)
**영구 사용:** 방법 2 (인증서 설치)
**ADB 가능:** 방법 3 (Port Forwarding)

## 문제 해결

### "Relaunch" 버튼이 안 보이면
- Chrome 완전히 종료 (최근 앱에서 스와이프)
- 다시 실행

### 여전히 에러가 나면
- Chrome 데이터 삭제
- 설정 → 앱 → Chrome → 저장공간 → 캐시 삭제

### IP 주소가 다르면
- 노트북에서 `ipconfig` 실행
- WiFi IPv4 주소 확인
- Chrome 플래그에 정확한 IP 입력
