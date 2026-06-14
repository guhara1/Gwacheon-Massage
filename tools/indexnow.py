#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 — 빙·네이버·얀덱스에 한 번에 전달.

IndexNow는 한 곳(api.indexnow.org)에 보내면 참여 검색엔진(Microsoft Bing,
Naver, Yandex, Seznam 등)에 자동으로 전파된다. 표준 라이브러리만 사용한다.

사용법:
  python3 tools/indexnow.py                # sitemap.xml 의 모든 URL 통보
  python3 tools/indexnow.py https://gwacheon-massage.pages.dev/gwacheon/...   # 특정 URL만

글(페이지)을 새로 올리거나 수정한 직후 실행하면 가장 빠르게 반영된다.
"""
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def submit(urls):
    base = BASE_URL.rstrip("/")
    host = base.split("://", 1)[-1]
    payload = {
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{base}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        code = resp.getcode()
    # 200 OK, 202 Accepted 는 정상 (202 는 키 확인 대기)
    print(f"IndexNow → {code}  ({len(urls)} URLs)")
    print("  키 파일이 접속 가능한지 확인:", payload["keyLocation"])
    return code


if __name__ == "__main__":
    urls = sys.argv[1:] or sitemap_urls()
    if not urls:
        print("통보할 URL이 없습니다. 먼저 python3 build.py 를 실행하세요.")
        sys.exit(1)
    submit(urls)
