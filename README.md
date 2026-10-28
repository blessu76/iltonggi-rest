# iltonggi.ipe.rest

일통기 웹사이트(GitHub Pages, 11개 언어). 페이지는 `content/*.json` 에서 `scripts/build_site.py` 로 생성한다(생성물은 손으로 고치지 않는다).

## 새 TestFlight 빌드를 릴리즈 노트에 올리기
1. `content/releases.json` 의 `entries` 맨 위에 항목을 더한다: `build`("1.0.0+N") · `at`("2026-10-29 06:12", KST) · `ko`/`en` 문장 배열(플레이어가 알아볼 말 2~4줄; 업로드 중이면 `"state":"uploading"`, 올라가면 지운다).
2. `python3 scripts/build_site.py && python3 -m unittest discover -s tests` — 그린이면 커밋·push(main 에 바로 push, Actions 가 배포).
3. 넣지 않는 것: 가격·커밋 해시·내부 경로·시크릿·공개 전 과금 상품 이름·미정 일정. 다른 9개 언어 페이지는 영어 본문을 자동으로 보여 준다.

날씨: `scripts/fetch_weather.py` 가 Actions 에서 매시 `weather.json` 을 만든다(`regions.json` 24곳).
