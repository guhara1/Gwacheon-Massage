#!/usr/bin/env python3
"""색인 통보 원클릭 — 빌드 후 한 번에 모든 검색엔진에 알림.

순서:
  1. IndexNow 로 빙·네이버·얀덱스에 통보 (의존성 없음)
  2. GOOGLE_APPLICATION_CREDENTIALS 가 설정돼 있으면 구글 Indexing API 통보

배포 워크플로 예:
  python3 build.py && python3 tools/notify_all.py

참고: 예전 sitemap ping(google.com/ping, bing.com/ping)은 2023년에
구글·빙 모두 폐기했습니다. 그래서 IndexNow + Indexing API + Search Console
사이트맵 등록 조합이 현재 가장 빠른 색인 경로입니다.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # tools/ (indexnow, google_indexing)
sys.path.insert(0, os.path.dirname(_HERE))      # 프로젝트 루트 (content)

import indexnow  # noqa: E402


def main():
    urls = indexnow.sitemap_urls()
    if not urls:
        sys.exit("통보할 URL이 없습니다. 먼저 python3 build.py 를 실행하세요.")

    print("== IndexNow (빙·네이버·얀덱스) ==")
    try:
        indexnow.submit(urls)
    except Exception as e:
        print("IndexNow 실패:", e)

    print("\n== 구글 Indexing API ==")
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        try:
            import google_indexing
            google_indexing.main(urls)
        except SystemExit as e:
            print(e)
        except Exception as e:
            print("구글 Indexing API 실패:", e)
    else:
        print("건너뜀: GOOGLE_APPLICATION_CREDENTIALS 미설정 "
              "(tools/google_indexing.py 안내 참고)")


if __name__ == "__main__":
    main()
