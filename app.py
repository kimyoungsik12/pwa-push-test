from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from pywebpush import webpush, WebPushException
import json
import os

app = Flask(__name__)
CORS(app)

# VAPID keys - 실제 운영시에는 환경변수로 관리
VAPID_PUBLIC_KEY = "BOIlytts6rwQVQYV1zATL7ohdB2clT0mjaJVF7ZqqstD9Lrvw0lGT86FS6TSoX94Vf2rIrCZIxh5f43VAnFvEWk"
VAPID_PRIVATE_KEY = "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgy4AG5fgYxtF9oCgZb9J2YKNpv7VasPQwDzq1FuZjt2OhRANCAATiJcrbbOq8EFUGFdcwEy-6IXQdnJU9Jo2iVRe2aqrLQ_S678NJRk_OhUuk0qF_eFX9qyKwmSMYeX-N1QJxbxFp"
VAPID_CLAIMS = {
    "sub": "mailto:test@example.com"
}

# 구독 정보 저장 파일
SUBSCRIPTION_FILE = 'subscriptions.json'

# 구독 정보 로드
def load_subscriptions():
    if os.path.exists(SUBSCRIPTION_FILE):
        try:
            with open(SUBSCRIPTION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

# 구독 정보 저장
def save_subscriptions(subs):
    with open(SUBSCRIPTION_FILE, 'w', encoding='utf-8') as f:
        json.dump(subs, f, indent=2)

# 서버 시작 시 구독 정보 로드
subscriptions = load_subscriptions()
print(f"📥 저장된 구독 정보 로드: {len(subscriptions)}개")

@app.route('/')
def index():
    """메인 페이지"""
    response = app.make_response(render_template('index.html'))
    # 캐시 방지 헤더 추가
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/sw.js')
def service_worker():
    """Service Worker 파일 제공 (루트 경로에서)"""
    static_folder = os.path.join(app.root_path, 'static')
    response = send_from_directory(static_folder, 'sw.js')
    response.headers['Content-Type'] = 'application/javascript; charset=utf-8'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

@app.route('/vapid-public-key')
def vapid_public_key():
    """VAPID 공개키 반환"""
    return jsonify({"publicKey": VAPID_PUBLIC_KEY})

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """푸시 알림 구독 등록"""
    subscription = request.get_json()
    endpoint = subscription.get('endpoint')

    # endpoint 기준으로 중복 확인 (같은 기기/브라우저는 같은 endpoint)
    existing = None
    for idx, sub in enumerate(subscriptions):
        if sub.get('endpoint') == endpoint:
            existing = idx
            break

    if existing is not None:
        # 기존 구독 업데이트 (키가 변경될 수 있음)
        subscriptions[existing] = subscription
        save_subscriptions(subscriptions)
        print(f"🔄 구독 정보 업데이트: {len(subscriptions)}개")
        return jsonify({"success": True, "message": "구독이 업데이트되었습니다.", "updated": True})
    else:
        # 새 구독 추가
        subscriptions.append(subscription)
        save_subscriptions(subscriptions)
        print(f"✅ 새로운 구독 등록: {len(subscriptions)}개")
        return jsonify({"success": True, "message": "구독이 등록되었습니다.", "updated": False})

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """푸시 알림 구독 해제"""
    subscription = request.get_json()

    if subscription in subscriptions:
        subscriptions.remove(subscription)
        save_subscriptions(subscriptions)
        print(f"❌ 구독 해제: {len(subscriptions)}개 남음")

    return jsonify({"success": True, "message": "구독이 해제되었습니다."})

@app.route('/send-notification', methods=['POST'])
def send_notification():
    """모든 구독자에게 푸시 알림 전송"""
    data = request.get_json()
    title = data.get('title', '테스트 알림')
    body = data.get('body', '푸시 알림 테스트입니다.')

    if not subscriptions:
        return jsonify({"success": False, "message": "구독자가 없습니다."})

    notification_payload = json.dumps({
        "title": title,
        "body": body,
        "icon": "/static/icon.png",
        "badge": "/static/badge.png"
    })

    success_count = 0
    failed_count = 0

    for subscription in subscriptions[:]:  # 복사본으로 순회
        try:
            webpush(
                subscription_info=subscription,
                data=notification_payload,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            success_count += 1
        except WebPushException as e:
            print(f"푸시 전송 실패: {e}")
            failed_count += 1
            # 구독이 만료된 경우 제거
            if e.response and e.response.status_code == 410:
                subscriptions.remove(subscription)
                save_subscriptions(subscriptions)

    return jsonify({
        "success": True,
        "message": f"알림 전송 완료 (성공: {success_count}, 실패: {failed_count})"
    })

@app.route('/cleanup-duplicates', methods=['POST'])
def cleanup_duplicates():
    """중복 구독 제거"""
    global subscriptions

    before_count = len(subscriptions)

    # endpoint 기준으로 중복 제거
    seen_endpoints = set()
    unique_subscriptions = []

    for sub in subscriptions:
        endpoint = sub.get('endpoint')
        if endpoint and endpoint not in seen_endpoints:
            seen_endpoints.add(endpoint)
            unique_subscriptions.append(sub)

    subscriptions = unique_subscriptions
    save_subscriptions(subscriptions)

    removed = before_count - len(subscriptions)

    print(f"🧹 중복 제거: {before_count}개 → {len(subscriptions)}개 (제거: {removed}개)")

    return jsonify({
        "success": True,
        "before": before_count,
        "after": len(subscriptions),
        "removed": removed
    })

@app.route('/test-notification')
def test_notification():
    """테스트 알림 즉시 전송"""
    if not subscriptions:
        return jsonify({"success": False, "message": "구독자가 없습니다."})

    notification_payload = json.dumps({
        "title": "🔔 테스트 알림",
        "body": "iPhone Safari 푸시 알림이 정상 작동합니다!",
        "icon": "/static/icon.png"
    })

    try:
        webpush(
            subscription_info=subscriptions[0],
            data=notification_payload,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
        return jsonify({"success": True, "message": "테스트 알림 전송 성공!"})
    except WebPushException as e:
        return jsonify({"success": False, "message": f"전송 실패: {str(e)}"})

if __name__ == '__main__':
    import socket

    # 로컬 IP 주소 출력
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print("\n" + "="*60)
    print("🚀 Push Notification Test Server (HTTPS)")
    print("="*60)
    print(f"\n📍 로컬 네트워크 주소: https://{local_ip}:5000")
    print(f"📍 로컬호스트: https://localhost:5000")
    print("\n💡 iPhone Safari 접속 방법:")
    print(f"   1. Safari에서 https://{local_ip}:5000 접속")
    print("   2. '이 연결은 비공개 연결이 아닙니다' → '자세히 보기' → '웹 사이트 방문'")
    print("   3. 홈 화면에 추가 (공유 버튼 → 홈 화면에 추가)")
    print("   4. 홈 화면 아이콘으로 실행\n")
    print("="*60 + "\n")

    # SSL 인증서 파일 확인
    if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
        print("❌ SSL 인증서가 없습니다!")
        print("📝 다음 명령으로 인증서를 생성하세요:")
        print("   python generate_cert.py\n")
        exit(1)

    # HTTPS로 서버 실행
    app.run(
        host='0.0.0.0',
        port=5000,
        ssl_context=('cert.pem', 'key.pem'),
        debug=True
    )
