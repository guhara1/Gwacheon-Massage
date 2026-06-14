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

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `python3 build.py` 재실행 (canonical·sitemap·robots.txt에 반영됨)
3. Google Search Console·네이버 서치어드바이저에 `sitemap.xml` 제출
