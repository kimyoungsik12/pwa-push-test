"""
자체 서명 SSL 인증서 생성 스크립트
iPhone Safari는 로컬 네트워크에서도 HTTPS 필요
"""
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import datetime
import socket
import ipaddress

print("🔒 SSL 인증서 생성 중...")

# 개인키 생성
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# 현재 컴퓨터의 호스트명과 IP 가져오기
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"📍 호스트명: {hostname}")
print(f"📍 로컬 IP: {local_ip}")

# 인증서 주체 정보
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "KR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Seoul"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Seoul"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Push Test"),
    x509.NameAttribute(NameOID.COMMON_NAME, local_ip),
])

# 인증서 생성
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([
        x509.DNSName("localhost"),
        x509.DNSName(hostname),
        x509.IPAddress(ipaddress.ip_address(local_ip)),
        x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
    ]),
    critical=False,
).sign(private_key, hashes.SHA256(), default_backend())

# 개인키 파일 저장
with open("key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# 인증서 파일 저장
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ SSL 인증서 생성 완료!")
print("\n📄 생성된 파일:")
print("   - cert.pem (인증서)")
print("   - key.pem (개인키)")
print("\n⚠️  iPhone에서 인증서 신뢰 설정 필요:")
print(f"   1. Safari에서 https://{local_ip}:5000 접속")
print("   2. '이 연결은 비공개 연결이 아닙니다' 경고 → '자세히 보기'")
print("   3. '웹 사이트 방문' 클릭")
print("   4. 또는 설정 > 일반 > 정보 > 인증서 신뢰 설정에서 활성화")
