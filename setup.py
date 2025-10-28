"""
원클릭 설정 스크립트
VAPID 키 생성 → app.py 자동 업데이트
"""
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
import re

print("🔑 VAPID 키 생성 중...")

# VAPID 키 생성 (cryptography 직접 사용)
private_key_obj = ec.generate_private_key(ec.SECP256R1(), default_backend())

# Private key 추출
private_key_bytes = private_key_obj.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
private_key = base64.urlsafe_b64encode(private_key_bytes).strip(b'=').decode('utf-8')

# Public key 추출
public_key_obj = private_key_obj.public_key()
public_key_bytes = public_key_obj.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)
public_key = base64.urlsafe_b64encode(public_key_bytes).strip(b'=').decode('utf-8')

print("✅ VAPID 키 생성 완료!")
print(f"\nPublic Key: {public_key}")
print(f"Private Key: {private_key[:50]}...")

# app.py 자동 업데이트
print("\n📝 app.py 업데이트 중...")

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 키 교체
content = re.sub(
    r'VAPID_PUBLIC_KEY = ".*"',
    f'VAPID_PUBLIC_KEY = "{public_key}"',
    content
)
content = re.sub(
    r'VAPID_PRIVATE_KEY = ".*"',
    f'VAPID_PRIVATE_KEY = "{private_key}"',
    content
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ app.py 업데이트 완료!")
print("\n🚀 이제 'python app.py' 명령으로 서버를 실행하세요!")
