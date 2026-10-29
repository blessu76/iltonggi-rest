# iltonggi.ipe.rest

일통기 웹사이트(GitHub Pages, 11개 언어). 페이지는 `content/*.json` 에서 `scripts/build_site.py` 로 생성한다(생성물은 손으로 고치지 않는다).

## 새 TestFlight 빌드를 릴리즈 노트에 올리기
빠른 길: `scripts/add_release.sh <빌드번호> <notes.md> [shots폴더]` — notes.md 는 `at: 날짜시각`(선택) + `## ko`/`## en` 아래 `- ` 불릿. shots폴더에 `map.png`·`march.png` 가 있으면 홈 화면 사진을 교체(1200×554 로 자름). 같은 빌드를 다시 넣으면 덮어쓴다. 아래는 손으로 하는 길.
1. `content/releases.json` 의 `entries` 맨 위에 항목을 더한다: `build`("1.0.0+N") · `at`("2026-10-29 06:12", KST) · `ko`/`en` 문장 배열(플레이어가 알아볼 말 2~4줄; 업로드 중이면 `"state":"uploading"`, 올라가면 지운다).
2. `python3 scripts/build_site.py && python3 -m unittest discover -s tests` — 그린이면 커밋·push(main 에 바로 push, Actions 가 배포).
3. 넣지 않는 것: 가격·커밋 해시·내부 경로·시크릿·공개 전 과금 상품 이름·미정 일정. 다른 9개 언어 페이지는 영어 본문을 자동으로 보여 준다.

날씨: `scripts/fetch_weather.py` 가 Actions 에서 매시 `weather.json` 을 만든다(`regions.json` 24곳).

## 블로그 (제작과정 · 매일 12:00 KST 자동 발행)
경로 `/blog/`(목록·10편씩 쪽 나누기 `/blog/page/N/`) · `/blog/<slug>/`(글) · `/blog/feed.xml`(RSS, 영어판). 11개 언어(`/<lang>/blog/…`), 슬러그는 모든 언어 같음. 글마다 canonical + 11개 언어 hreflang + x-default + JSON-LD BlogPosting, 게시 시각은 `ipe-localtime`. 헤더·푸터 메뉴에 「블로그」. 빌드는 `build_site.py` 안에서 함께 돈다(`scripts/blog.py`). sitemap·robots·RSS 는 「전 사이트 공통 SEO 가이드」가 오면 맞춘다.

**글 한 편 = 11개 파일** `en ko ja zh es pt id ru vi fr de` `.md` (en·ko 원문, 나머지 9개는 `translation_of: en|ko` → 「AI 번역」 표시 + 원문 링크). front matter(한 줄씩 `키: 값`):
```
---
title: …
description: …            # 한 문장
date: 2026-10-30          # 대기열에서는 아무 날짜나 — 발행 때 오늘(KST)로 덮어씀
slug: my-slug             # 영문 kebab, 모든 언어 같게 · 폴더 이름과 같게
lang: ko                  # 파일 이름과 같게
translation_of: en        # en·ko 원문에는 쓰지 않음
---
본문: 문단 · ## / ### 제목 · - 목록 · 1. 목록 · > 인용 · **굵게** · *기울임* · [글](/사이트내/경로) · ![설명](/assets/blog/파일.webp)
```
외부 링크·코드·표는 쓸 수 없다(`/assets/blog/` 그림은 파일을 같이 커밋).

**대기열에 넣는 법 (Quill 작성 → Dane 검수 끝난 글만)**
1. `content/blog/queue/<NNN>-<slug>/` 폴더를 만들고 11개 `.md` 를 넣는다. NNN = 순서(`001`, `002`, … 작은 것부터 하루 1편). `published:` 는 쓰지 않는다(발행 스크립트가 도장).
2. `python3 scripts/blog.py` — 11개 파일·front matter·본문 문법·**안전 린트**(코드/URL/내부 경로/파일명/키 같은 토큰/이메일/가격/내부 도구 낱말)를 대기열 전체에 검사. 통과해야 커밋한다.
3. 대기열 폴더는 **발행 스크립트만 비운다**(사람은 더하기만). 이미 올라간 글을 고치려면 `content/blog/posts/<slug>/` 파일을 직접 고치고(`updated: …+09:00` 추가) 빌드.

**발행**: `python3 scripts/publish_blog.py` (`--dry-run` 확인만 · `--no-push` · `--slug` · `--force` 하루 2편). 대기열 첫 글을 `posts/` 로 옮기고 `date`·`published`(+09:00) 도장 → 빌드 → `--check` → 테스트 → 커밋 → `pull --rebase` → `push origin HEAD:main`. 하루 1편(이미 오늘 올렸으면 건너뜀)·대기열이 비면 아무것도 안 함·실패하면 되돌리고 종료코드 1. 번호 `No. N` 은 게시 순.
**자동 실행**: 맥미니 launchd 가 매일 12:00 KST(12:30·13:30 재시도) — 설치·확인은 `scripts/launchd/README.md`.
