#!/usr/bin/env python3
"""구글 Indexing API 즉시 색인 통보 (구글은 IndexNow 미참여).

구글에 URL 갱신을 즉시 알리는 공식 경로다. 서비스 계정 인증이 필요하다.

준비 (최초 1회):
  1. Google Cloud 콘솔에서 프로젝트 생성 → "Indexing API" 사용 설정
  2. 서비스 계정 생성 → JSON 키 다운로드
  3. Google Search Console에서 해당 속성의 '소유자'로 서비스 계정 이메일 추가
  4. 의존성 설치:  pip install -r tools/requirements.txt

사용법:
  GOOGLE_APPLICATION_CREDENTIALS=service-account.json \
      python3 tools/google_indexing.py            # sitemap 전체
  GOOGLE_APPLICATION_CREDENTIALS=service-account.json \
      python3 tools/google_indexing.py https://...  # 특정 URL

참고: 일일 할당량 기본 200건. 페이지가 적은 사이트라 전체 제출도 여유롭다.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


def sitemap_urls():
    with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def main(urls):
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("의존성이 필요합니다:  pip install -r tools/requirements.txt")

    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path or not os.path.exists(cred_path):
        sys.exit("환경변수 GOOGLE_APPLICATION_CREDENTIALS 에 서비스 계정 JSON 경로를 지정하세요.")

    creds = service_account.Credentials.from_service_account_file(
        cred_path, scopes=SCOPES)
    session = AuthorizedSession(creds)

    ok = 0
    for url in urls:
        r = session.post(ENDPOINT, json={"url": url, "type": "URL_UPDATED"})
        status = "OK" if r.status_code == 200 else f"ERR {r.status_code}"
        if r.status_code == 200:
            ok += 1
        else:
            print("  ", r.text[:200])
        print(f"{status}  {url}")
    print(f"\n구글 Indexing API: {ok}/{len(urls)} 성공")


if __name__ == "__main__":
    urls = sys.argv[1:] or sitemap_urls()
    if not urls:
        sys.exit("통보할 URL이 없습니다. 먼저 python3 build.py 를 실행하세요.")
    main(urls)
