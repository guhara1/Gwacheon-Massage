# 간다GO — 과천 출장마사지·과천시 홈타이 안내 사이트

과천시 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
예약전화: **0508-202-4719**

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·sitemap 생성)
content/
  site.py           # 상호·전화·BASE_URL·행정동/역 목록·메뉴 구조
  main.py           # 메인 페이지 (+ Organization/WebPage/BreadcrumbList/FAQPage JSON-LD)
  areas.py          # 행정동별: 중앙·갈현·별양·부림·과천·문원·원문 (7개)
  stations.py       # 지하철역별: 과천·정부과천청사·선바위·경마공원·대공원 (5개)
  info.py           # 예약 안내·이용 전 확인사항·홈타이 이용 가이드·고객센터·약관
  pricing.py        # 공용 요금 블록
assets/             # CSS, 모바일 내비 JS, 파비콘, OG 이미지
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## 사이트 구조 (과천시 메인 → 행정동 → 지하철역)

```
/                                              과천 출장마사지 메인 (허브)
/gwacheon/{행정동}-dong-chuljangmassage/        행정동 7개
/gwacheon/{역}-station-chuljangmassage/         지하철역 5개
/reservation/  /precautions/  /guide/          예약·이용 전 확인·홈타이 가이드
/support/  /privacy/  /terms/                   고객센터·약관
```

총 18개 색인 페이지 + 약관 2종(noindex) = 메인 1 / 행정동 7 / 역 5 / 안내 5.

## SEO 운영 원칙 (빌드·작성에 반영됨)

- **과천시는 행정구가 없으므로 행정구 페이지를 만들지 않는다** — 메인에서 바로 행정동으로 연결
- 1동·2동처럼 번호가 붙은 행정동이 없어 7개 행정동을 각각 대표 페이지로 운영
- 역은 역 1개당 페이지 1개 — 환승·출구별 분할 페이지 없음
- 지역+역+테마 조합 페이지 없음 (도어웨이 방지)
- 모든 디스크립션은 **80자 이내**
- 타이틀은 페이지마다 고유 (지역명 출장마사지 선두) — 지역 내 중복·도어웨이 방지
- 본문 **2,000자 미만 페이지는 자동 noindex** 처리되고 sitemap에서 제외 (요금 블록 제외 측정)
- 페이지 간 유사도 최소화 (4-gram Jaccard < 0.11 확인)
- 실제 오프라인 주소가 없으므로 LocalBusiness Schema는 사용하지 않음 (Organization만 사용)

## 색인 가속 (빠른 인덱싱)

배포 도메인: **https://gwacheon-massage.pages.dev** (Cloudflare Pages)

빌드가 자동 생성하는 색인용 파일:

```
sitemap.xml                       lastmod·changefreq·priority 포함 (색인 17개)
rss.xml                           네이버 서치어드바이저 RSS 제출용
robots.txt                        Yeti(네이버)·Googlebot·bingbot·Daum 명시 + 사이트맵
37988d0653232654fac055b54bb0c6d9.txt   IndexNow 키 파일 (루트 접근용)
```

### 1) 검색엔진 등록 (최초 1회)

- **구글 Search Console**: 속성 등록 → `sitemap.xml` 제출
- **네이버 서치어드바이저**: 사이트 등록(메인에 인증 메타 삽입 완료) → `sitemap.xml` + `rss.xml` 제출
- **빙 Webmaster Tools**: `sitemap.xml` 제출 (또는 GSC에서 가져오기)

### 2) IndexNow — 글 올릴 때마다 즉시 통보 (빙·네이버·얀덱스)

키 파일이 도메인 루트에서 열려야 합니다: `https://gwacheon-massage.pages.dev/37988d0653232654fac055b54bb0c6d9.txt`

```bash
python3 build.py
python3 tools/indexnow.py                 # 사이트맵 전체 통보
python3 tools/indexnow.py https://gwacheon-massage.pages.dev/gwacheon/...  # 특정 URL만
```

### 3) 구글 Indexing API — 구글 즉시 통보 (구글은 IndexNow 미참여)

```bash
pip install -r tools/requirements.txt
# Google Cloud: Indexing API 사용 설정 → 서비스 계정 JSON 발급
# Search Console 속성에 서비스 계정 이메일을 '소유자'로 추가
GOOGLE_APPLICATION_CREDENTIALS=service-account.json python3 tools/google_indexing.py
```

### 4) 원클릭 통보 (빌드 후 권장 워크플로)

```bash
python3 build.py && python3 tools/notify_all.py
```

IndexNow + (자격증명 있으면) 구글 Indexing API를 한 번에 실행합니다.
※ 예전 sitemap ping(google.com/ping)은 2023년 폐기되어, 위 조합이 현재 가장 빠른 경로입니다.

## 배포 전 체크리스트

1. `content/site.py`의 `BASE_URL` 확인 (현재 pages.dev 도메인 적용됨)
2. `python3 build.py` 실행 (canonical·sitemap·rss·robots·IndexNow 키에 반영)
3. 배포 후 IndexNow 키 파일 접속 확인 → `tools/notify_all.py` 실행
4. 구글/네이버/빙에 사이트맵·RSS 제출
