# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://gwacheon-massage.pages.dev"

BRAND = "간다GO"
BRAND_MARK = "G"  # 헤더 브랜드 마크에 들어가는 한 글자
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 사이트 설명 (RSS·메타 공용)
SITE_DESC = "과천시 전지역 방문 출장마사지·홈타이 예약 안내. 행정동·역세권·이용 기준을 정리했습니다."

# IndexNow 키 — 빌드 시 루트에 {INDEXNOW_KEY}.txt 파일로 생성된다.
# 빙·네이버·얀덱스에 즉시 색인 통보할 때 사용한다.
INDEXNOW_KEY = "37988d0653232654fac055b54bb0c6d9"

# 행정동 (7개) — slug, 표시명
DONGS = [
    ("jungang-dong-chuljangmassage", "중앙동"),
    ("galhyeon-dong-chuljangmassage", "갈현동"),
    ("byeoryang-dong-chuljangmassage", "별양동"),
    ("burim-dong-chuljangmassage", "부림동"),
    ("gwacheon-dong-chuljangmassage", "과천동"),
    ("munwon-dong-chuljangmassage", "문원동"),
    ("wonmun-dong-chuljangmassage", "원문동"),
]

# 지하철역 (5개) — slug, 표시명
STATIONS = [
    ("gwacheon-station-chuljangmassage", "과천역"),
    ("government-complex-gwacheon-station-chuljangmassage", "정부과천청사역"),
    ("seonbawi-station-chuljangmassage", "선바위역"),
    ("seoul-racecourse-park-station-chuljangmassage", "경마공원역"),
    ("seoul-grand-park-station-chuljangmassage", "대공원역"),
]

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("홈", "/", []),
    ("과천 출장마사지", "/", [
        ("과천 출장마사지 안내", "/#service"),
        ("과천 홈타이 안내", "/#hometai"),
        ("전지역 방문 안내", "/#coverage"),
        ("예약 안내", "/reservation/"),
        ("이용 전 확인사항", "/precautions/"),
        ("홈타이 이용 가이드", "/guide/"),
    ]),
    ("지역별 안내", "/#areas", [
        (name, f"/gwacheon/{slug}/") for slug, name in DONGS
    ]),
    ("지하철역별 안내", "/#stations", [
        (name, f"/gwacheon/{slug}/") for slug, name in STATIONS
    ]),
    ("예약 안내", "/reservation/", []),
    ("이용 전 확인사항", "/precautions/", []),
    ("홈타이 이용 가이드", "/guide/", []),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("개인정보 처리방침", "/privacy/"),
        ("이용약관", "/terms/"),
    ]),
]
